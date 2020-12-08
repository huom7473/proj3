#!/usr/bin/python3
# NAME: Michael Huo, Tygan Zeng
# EMAIL: huom7473@ucla.edu, zengtygan@gmail.com
# ID: 705408359, 705391071
import sys

def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} [file.csv]", file=sys.stderr)
        return 1

    linesdict = {}
    
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

    print(f"block size (bytes): {linesdict['SUPERBLOCK'][0][3]}")
    
if __name__ == "__main__":
    main()
