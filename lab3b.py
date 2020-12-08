#!/usr/bin/python3
# NAME: Michael Huo, Tygan Zeng
# EMAIL: huom7473@ucla.edu, zengtygan@gmail.com
# ID: 705408359, 705391071
import sys


linesdict = {}

block_free_list_set = set()
block_allocated_set = set()


def generate_free_list():
    for i in linesdict['BFREE']:
        block_free_list_set.add(int(i[1]))

def check_unreferenced_blocks():
    for i in range(reserved_boundary, num_blocks):
        if (not i in block_free_list_set) and (not i in block_allocated_set):
            print(f"UNREFERENCED BLOCK {i}")
        if (i in block_free_list_set) and (i in block_allocated_set):
            print(f"ALLOCATED BLOCK {i} ON FREELIST")

def scan_blocks():
    boundary = 0
    for i in linesdict['INODE']:
        if i[2] == 'f' or i[2] == 'd':
            for j in range(15):
                if int(i[12+j]) < 0 or int(i[12+j]) > num_blocks:
                    if j < 12:
                        print(f"INVALID BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 12:
                        print(f"INVALID INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 13:
                        print(f"INVALID DOUBLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET 268")
                    elif j == 14:
                        print(f"INVALID TRIPLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET 65804")
                elif int(i[12+j]) > 0 and int(i[12+j]) < reserved_boundary:
                    if j < 12:
                        print(f"RESERVED BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 12:
                        print(f"RESERVED INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 13:
                        print(f"RESERVED DOUBLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET 268")
                    elif j == 14:
                        print(f"RESERVED TRIPLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET 65804")
                else:
                    block_allocated_set.add(int(i[12+j]))
    
    print("second loop")        
    for i in linesdict['INDIRECT']:
        if int(i[5]) < 0 or int(i[5]) > num_blocks: 
            print(i[2])
            if i[2] == '1':
                print(f"INVALID INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif i[2] == '2':
                print(f"INVALID DOUBLE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif i[2] == '3':
                print(f"INVALID TRIPLE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
        else:
            block_allocated_set.add(int(i[5]))


    return;

def main():

    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} [file.csv]", file=sys.stderr)
        return 1
    
    try:
        with open(sys.argv[1]) as csv:
            for line in csv:
                type = line.split(',')[0]
                if type not in linesdict:
                    linesdict[type] = []
                linesdict[type].append(tuple(line.split(',')))
    except FileNotFoundError:
        print(f"{sys.argv[0]}: error opening file {sys.argv[1]}: file doesn't exist",
              file=sys.stderr)
        return 1
    # todo: make error handling handle all errors
    global num_blocks
    num_blocks = int(linesdict['SUPERBLOCK'][0][1])

    block_size = int(linesdict['SUPERBLOCK'][0][3])
    inode_size = int(linesdict['SUPERBLOCK'][0][4])
    inodes_per_block = int(block_size/inode_size)
    inodes_per_group = int(linesdict['SUPERBLOCK'][0][6])
    global reserved_boundary
    reserved_boundary = int(inodes_per_group/inodes_per_block) + int(linesdict['GROUP'][0][8])
    print(f"Reserved boundary is {reserved_boundary}")

    generate_free_list()
    scan_blocks()
    print(block_allocated_set)
    print(block_free_list_set)
    check_unreferenced_blocks()
    
if __name__ == "__main__":
    main()
