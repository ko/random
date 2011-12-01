#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#define sstrncpy(dst, src) strncpy(dst,src,sizeof(dst)-1)

int layer2(char * str) {
    sstrncpy(str, "1234567890");
    printf("sizeof(str) is %" PRIuPTR "\n", sizeof(str));
    printf("strlen(str) is %zu\n", strlen(str));
    return 1;
}

int layer1(char * str) {
    sstrncpy(str, "stewardess");
    layer2(str);
    return 1;
}

int main(void) {
    char buf[200];
    char *c = buf;

    memset(buf, 0, sizeof(buf));
    layer1(buf);
    printf ("buf is: %s\n", buf);

    memset(c , 0, sizeof(c));
    layer1(c);
    printf ("c is: %s\n", c);

    return 0;
}
