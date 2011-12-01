#include <string.h>
#include <stdio.h>

# define safer_strncpy(dst, src, dst_size_minus_one) \
    do { \
        strncpy(dst,src,dst_size_minus_one); \
        dst[dst_size_minus_one] = '\0'; \
    } while (0);

int main(void)
{
    char a[20] = "AAAAAAAAAAAAAAAAAAA";
    safer_strncpy(a, "NULL", 4);
    printf ("%s\n", a);
    return 0;
}
