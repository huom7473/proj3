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

int main(int argc, char **argv) {
    if (argc != 2) { //./lab3a [img name]
        fprintf(stderr, "usage: %s [image]\n", argv[0]);
        exit(1);
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        fprintf(stderr, "%s: error opening image file %s: %s\n", argv[0], argv[1], strerror(errno));
        exit(1);
    }

    fprintf(stderr, "size of super block struct: %lu\n", sizeof(super_block)); //block size ?
    super_block* sb = malloc(sizeof(super_block));
    pread(fd, sb, sizeof(super_block), 1024); //read super block
    unsigned long bsize = EXT2_MIN_BLOCK_SIZE << sb->s_log_block_size;
    fprintf(stderr, "size of block according to superblock: %lu\n", bsize);
    exit(0);
}