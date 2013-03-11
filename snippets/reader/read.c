#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>

#define OUTFILE "/tmp/reader.bin"
#define BYTE_MAX 255
#define FILE_SZ (4194304 / 2)
//#define BLOCK_SZ (FILE_SZ / sizeof(short))
#define BLOCK_SZ 1024
#define BLOCK_NO 4096

#define DEBUG

void writeEm() 
{
    char * buf = NULL;
    short lo, hi;
    short word;
    unsigned int i = 0, j = 0, k = 0;
    int fd = -1;

    printf("writing...\n");

    unlink(OUTFILE);
    fd = open(OUTFILE, O_RDWR | O_CREAT);
    buf = (char*)malloc(sizeof(char) * BLOCK_SZ); 
    memset(buf, 0x41, BLOCK_SZ);

    for (hi = 0; hi <= BYTE_MAX; hi++) {
        for (lo = 0; lo <= BYTE_MAX; lo++) {
            // block contents
            word = (hi << 8) | lo;
            memset(buf, (char)word, BLOCK_SZ);
            write(fd, buf, BLOCK_SZ) ;
        }
    }
    close(fd);    

    printf("writing... done\n");
}

void readEm(void)
{
    char * buf = NULL;
    short lo, hi;
    short word;
    unsigned int i = 0, j = 0, k = 0;
    int fd = -1, rc = 0;
   
    printf("reading...\n");

    fd = open(OUTFILE, O_RDWR);
    buf = (char *)malloc(BLOCK_SZ);
    for (i = 0; i <= BYTE_MAX * BYTE_MAX; i++) {
        rc = read(fd, buf, BLOCK_SZ);
        if (rc != BLOCK_SZ) {
            printf("read fail,%s,%d,%d\n", strerror(errno), i, rc);
        } 
#ifdef DEBUGIT
        else {
            printf("read win,%d,%x\n", i, buf[1]);
        }
#endif
    }

    close(fd);

    printf("reading... done\n");
}

int main(void) 
{
    char write = 0;
    char read = 1;
    if (write) 
        writeEm();
    
    if (read) 
        readEm();

    return 0;
}
