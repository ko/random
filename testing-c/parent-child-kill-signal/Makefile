CC=gcc
CFLAGS=-Wall -g
OBJ_FILES=rent.o child.o

child:
	$(CC) child.c -o child

parent:
	$(CC) rent.c -o parent

all: child parent

clean:
	rm child parent
