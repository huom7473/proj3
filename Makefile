# NAME: Michael Huo, Tygan Zeng
# EMAIL: huom7473@ucla.edu, zengtygan@gmail.com
# ID: 705408359, 705391071

CC=gcc
CFLAGS=-Wall -Wextra

.PHONY: clean dist default

default: lab3a

lab3a: lab3a.c ext2_fs.h
	@$(CC) -o lab3a $(CFLAGS) lab3a.c

clean:
	@rm -f lab3a lab3a-705408359.tar.gz

dist:
	@tar -czf lab3a-705408359.tar.gz lab3a.c ext2_fs.h Makefile README
