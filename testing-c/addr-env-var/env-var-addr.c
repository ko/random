#include <stdlib.h>
#include <stdio.h>

int main() {
	
	const char * egg = "EGG";
	char * sc = getenv(egg);
	if (sc)
		printf ("%p\n", sc);
	else
		printf ("fail");
}
