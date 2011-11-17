#include <stdio.h>

int main (void) {

    char a[20] = "Hello world";
    char *b = a;
    printf ("b: %s\n", b);
    b = '\0';
    printf ("b: %s\n", b);
}
