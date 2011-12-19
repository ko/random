#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void f(int *ip)
{
    *ip = 5;
    return;
}

int allocstr(int len, char**retptr)
{
    char *p = malloc(len+1);
    if (p == NULL)
        return 0;
    *retptr = p;
    return 1;
}

int main(void) 
{
    int **ipp = NULL;
    int i = 5, j = 6, k = 7;
    int *ip1 = &i, *ip2 = &j;

    /* ipp points to ip1 which points to i
     * -    *ipp is ip1
     * -    **ipp is i (5)
     */
    ipp = &ip1;
    printf("ipp = &ip1: %d\n", **ipp);

    /* pointer pointed to by ipp (ip1) contains a copy of ip2
     * -    *ipp is ip1
     * -    **ipp (*ip1) is j (6)
     */
    *ipp = ip2;
    printf("*ipp = ip2: %d\n", **ipp);

    /* pointer pointed to by ipp (ip1) points to k
     * -    *ipp is ip1
     * -    **ipp (*ipl) is k (7)
     */
    *ipp = &k;
    printf("*ipp = &k: %d\n", **ipp);

    /* returning pointers from functions, via pointer arguments
     * rather than the formal return value
     */
    int m;
    f(&m);
    printf("f(&m): %d\n", m);

    char *string = "Hello, world!";
    char *copystr;
    if (allocstr(strlen(string), &copystr)) {
        strcpy(copystr, string);
        printf("%s\n", copystr);
    } else {
        fprintf(stderr, "OOM\n");
        return -1;
    }

    return 0;
}
