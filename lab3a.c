/* NAME: Michael Huo, Tygan Zeng */
/* EMAIL: huom7473@ucla.edu,  */
/* ID: 705408359,  */
#include <sys/types.h>
#include "ext2_fs.h" //include this after stdint.h to avoid typedef issues
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

typedef struct ext2_super_block super_block;
typedef struct ext2_group_desc group_desc;

super_block* sb; //access super block globally
group_desc* group; //assume we only need to deal with single groups
int fd;

unsigned long calculate_offset(unsigned block_num) {
    return block_num * (EXT2_MIN_BLOCK_SIZE << sb->s_log_block_size);
}

void read_super_block() {
    sb = malloc(sizeof(super_block));
    if (!sb) {
        fprintf(stderr, "%s: error in buffer allocation\n", argv[0]);
        exit(2);
    }

    pread(fd, sb, sizeof(super_block), 1024); //read super block

    if (sb->s_magic != EXT2_SUPER_MAGIC) {
        fprintf(stderr, "super block magic value check failed\n");
        exit(1);
    }
    
    unsigned int bsize = EXT2_MIN_BLOCK_SIZE << sb->s_log_block_size;
    fprintf(stderr, "size of block according to superblock: %d\n", bsize);
    fprintf(stdout, "SUPERBLOCK,%d,%d,%d,%d,%d,%d,%d\n",
            sb->s_blocks_count, sb->s_inodes_count, bsize, sb->s_inode_size,
            sb->s_blocks_per_group, sb->s_inodes_per_group, sb->s_first_ino);
}

void read_group() {
    group = malloc(sizeof(group_desc));
    if (!group) {
        fprintf(stderr, "%s: error in buffer allocation\n", argv[0]);
        exit(2);
    }
    
    pread(fd, group, sizeof(group_desc), calculate_offset(sb->s_first_data_block + 1));
    fprintf(stdout,"GROUP,%d,%d,%d,%d,%d,%d,%d,%d\n", 0,
            sb->s_blocks_count, sb->s_inodes_count, group->bg_free_blocks_count,
            group->bg_free_inodes_count, group->bg_block_bitmap, group->bg_inode_bitmap, group->bg_inode_table);
}

void scan_free_blocks() {
    unsigned int bsize = EXT2_MIN_BLOCK_SIZE << sb->s_log_block_size;
    unsigned char *buffer = malloc(bsize);
    if (!buffer) {
        fprintf(stderr, "%s: error in buffer allocation\n", argv[0]);
        exit(2);
    }

    pread(fd, buffer, bsize, calculate_offset(group->bg_block_bitmap));

    unsigned int byte, offset;
    for(unsigned i = 0; i < sb->s_blocks_per_group; ++i) {
        byte = i / 8; // 8 blocks represented per byte
        offset = i % 8; //offset from that byte
        if (!(buffer[byte] >> offset & 0x1)) { //find the right bit, if it's 0 the if statement is true
            fprintf(stdout, "BFREE,%u\n", i + 1); //I guess block # starts at 1
        }
    }
    free(buffer);
}

void scan_free_inodes() {
    unsigned int bsize = EXT2_MIN_BLOCK_SIZE << sb->s_log_block_size;
    unsigned char *buffer = malloc(bsize);
    if (!buffer) {
        fprintf(stderr, "%s: error in buffer allocation\n", argv[0]);
        exit(2);
    }

    pread(fd, buffer, bsize, calculate_offset(group->bg_inode_bitmap));

    unsigned int byte, offset;
    for(unsigned i = 0; i < sb->s_inodes_per_group; ++i) {
        byte = i / 8; // 8 blocks represented per byte
        offset = i % 8; //offset from that byte
        if (!(buffer[byte] >> offset & 0x1)) { //find the right bit, if it's 0 the if statement is true
            fprintf(stdout, "IFREE,%u\n", i + 1); //I guess block # starts at 1
        }
    }
    free(buffer);
}

int main(int argc, char **argv) {
    if (argc != 2) { //./lab3a [img name]
        fprintf(stderr, "usage: %s [image]\n", argv[0]);
        exit(1);
    }

    fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        fprintf(stderr, "%s: error opening image file %s: %s\n", argv[0], argv[1], strerror(errno));
        exit(1);
    }

    fprintf(stderr, "size of super block struct: %lu\n", sizeof(super_block)); //block size ?
    
    read_super_block();
    read_group();
    scan_free_blocks();
    scan_free_inodes();
    exit(0);
}