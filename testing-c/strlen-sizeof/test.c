#include <string.h>
#include <stdio.h>
#include <inttypes.h>

int main(void) {
    
    char a[20];
    memset(a, 0, 20);
    printf("sizeof is %" PRIuPTR "\n", sizeof(a));
    printf("strlen is %zu\n", strlen(a));
}
