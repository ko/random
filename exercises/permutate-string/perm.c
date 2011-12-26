#include <stdio.h>

void swap(char *one, char *two)
{
    char temp;
    temp = *one;
    *one = *two;    // [one] = [two]
    *two = temp;    // [two] = temp    
    return;
}

void permute(char *s, int start, int end)
{
    int i, j;
    if (start == end) {                     // base case 
        printf("%s\n", s);
    } else {
        for (i = start; i <= end; i++) {    
            swap((s+start), (s+i));         // swap(A,B)
            permute(s, start+1, end);       // permute("ABCD", 1, 3)
            swap((s+start), (s+i));         // swap(B,A) 
        }
    }
    return;
} 

int main(void)
{
    char a[] = "ABCD";
    permute(a, 0, 3);
    getchar();
    return 0;
}
