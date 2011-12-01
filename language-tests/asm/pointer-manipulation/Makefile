CC=gcc
CFLAGS=-S -masm=intel -m32
SRC=test.i

asm:
	$(CC) $(CFLAGS) $(SRC)

bin:
	$(CC) $(SRC) -o test

all: asm bin

clean:
	rm test.s test
