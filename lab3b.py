#!/usr/bin/python3
# NAME: Michael Huo, Tygan Zeng
# EMAIL: huom7473@ucla.edu, zengtygan@gmail.com
# ID: 705408359, 705391071
import sys


linesdict = {}

block_free_list_set = set()
inode_free_list_set = set()
block_allocated_set = set()
inode_allocated_set = set()
block_printed_set = set()
block_dictionary = dict()

def generate_free_list():
    for i in linesdict['BFREE']:
        block_free_list_set.add(i[1])
    for i in linesdict['IFREE']:
        inode_free_list_set.add(i[1])
    

def check_unreferenced_blocks():
    for i in range(reserved_boundary, num_blocks):
        if (i not in block_free_list_set) and (i not in block_allocated_set):
            print(f"UNREFERENCED BLOCK {i}")
        if (i in block_free_list_set) and (i in block_allocated_set):
            print(f"ALLOCATED BLOCK {i} ON FREELIST")

def check_inodes():
    for i in range(1, inode_start):
        if i in inode_free_list_set:
            print(f"ALLOCATED INODE {i} ON FREELIST")
    for i in range(inode_start, num_inodes):
        if (i not in inode_free_list_set) and (i not in inode_allocated_set):
            print(f"UNREFERENCED INODE {i}")
        if (i in inode_free_list_set) and (i in inode_allocated_set):
            print(f"ALLOCATED INODE {i} ON FREELIST")

def scan_blocks():
    boundary = 0
    for i in linesdict['INODE']:
        double_offset = 12 + block_size/4 # 4 is the size of a block pointer (unsigned 32 bit)
        triple_offset = double_offset + (block_size/4)**2
        if i[2] == 'f' or i[2] == 'd':
            for j in range(15):
                if i[12+j] < 0 or i[12+j] > num_blocks:
                    if j < 12:
                        print(f"INVALID BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 12:
                        print(f"INVALID INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 13:
                        print(f"INVALID DOUBLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {double_offset}")
                    elif j == 14:
                        print(f"INVALID TRIPLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {triple_offset}")
                elif i[12+j] > 0 and i[12+j] < reserved_boundary:
                    if j < 12:
                        print(f"RESERVED BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 12:
                        print(f"RESERVED INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 13:
                        print(f"RESERVED DOUBLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {double_offset}")
                    elif j == 14:
                        print(f"RESERVED TRIPLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {triple_offset}")
                else:
                    block_allocated_set.add(i[12+j])

                if i[12+j] in block_dictionary:
                    if j < 12:
                        print(f"DUPLICATE BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 12:
                        print(f"DUPLICATE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {j}")
                    elif j == 13:
                        print(f"DUPLICATE DOUBLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {double_offset}")
                    elif j == 14:
                        print(f"DUPLICATE TRIPLE INDIRECT BLOCK {i[12+j]} IN INODE {i[1]} AT OFFSET {triple_offset}")
                    block_printed_set.add(i[12+j])
                elif i[12+j] != 0:
                    if j < 12:
                        block_dictionary[i[12+j]] = (0, i[1], j)
                    elif j == 12: 
                        block_dictionary[i[12+j]] = (1, i[1], j)
                    elif j == 13:
                        block_dictionary[i[12+j]] = (2, i[1], 268)
                    elif j == 14:
                        block_dictionary[i[12+j]] = (3, i[1], 65804)
        
        inode_allocated_set.add(i[1])
                    
                
    
    # print("second loop")        
    for i in linesdict['INDIRECT']:
        if i[5] < 0 or i[5] > num_blocks: 
            print(i[2])
            if i[2] == '1':
                print(f"INVALID INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif i[2] == '2':
                print(f"INVALID DOUBLE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif i[2] == '3':
                print(f"INVALID TRIPLE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
        else:
            block_allocated_set.add(i[5])
        
        if i[5] in block_dictionary:
            if j < 12:
                print(f"DUPLICATE BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif j == 12:
                print(f"DUPLICATE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif j == 13:
                print(f"DUPLICATE DOUBLE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            elif j == 14:
                print(f"DUPLICATE TRIPLE INDIRECT BLOCK {i[5]} IN INODE {i[1]} AT OFFSET {i[3]}")
            block_printed_set.add(i[5])
        elif i[5] != 0:
            if j < 12:
                block_dictionary[i[5]] = (0, i[1], i[3])
            elif j == 12: 
                block_dictionary[i[5]] = (1, i[1], i[3])
            elif j == 13:
                block_dictionary[i[5]] = (2, i[1], i[3])
            elif j == 14:
                block_dictionary[i[5]] = (3, i[1], i[3])
            

    for i in block_printed_set:
        if block_dictionary[i][0] == 0:
            print(f"DUPLICATE BLOCK {i} IN INODE {block_dictionary[i][1]} AT OFFSET {block_dictionary[i][2]}")
        elif block_dictionary[i][0] == 1:
            print(f"DUPLICATE INDIRECT BLOCK {i} IN INODE {block_dictionary[i][1]} AT OFFSET {block_dictionary[i][2]}")
        elif block_dictionary[i][0] == 2:
            print(f"DUPLICATE DOUBLE BLOCK {i} IN INODE {block_dictionary[i][1]} AT OFFSET {block_dictionary[i][2]}")
        elif block_dictionary[i][0] == 3:
            print(f"DUPLICATE TRIPLE BLOCK {i} IN INODE {block_dictionary[i][1]} AT OFFSET {block_dictionary[i][2]}")

    return

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
                temp = []
                for field in line.split(','):
                    try:
                        temp.append(int(field))
                    except ValueError:
                        temp.append(field)
                linesdict[type].append(tuple(temp))
    except FileNotFoundError:
        print(f"{sys.argv[0]}: error opening file {sys.argv[1]}: file doesn't exist",
              file=sys.stderr)
        return 1
    # todo: make error handling handle all errors
    global num_blocks
    num_blocks = linesdict['SUPERBLOCK'][0][1]
    
    global num_inodes
    num_inodes = linesdict['SUPERBLOCK'][0][2]
    
    global block_size
    block_size = linesdict['SUPERBLOCK'][0][3]
    inode_size = linesdict['SUPERBLOCK'][0][4]
    inodes_per_block = block_size/inode_size # both are powers of 2
    inodes_per_group = linesdict['SUPERBLOCK'][0][6]

    global inode_start
    inode_start = linesdict['SUPERBLOCK'][0][7]

    global reserved_boundary
    reserved_boundary = int(inodes_per_group/inodes_per_block) + linesdict['GROUP'][0][8]

    generate_free_list()
    scan_blocks()
    check_unreferenced_blocks()
    check_inodes()
    
if __name__ == "__main__":
    main()
