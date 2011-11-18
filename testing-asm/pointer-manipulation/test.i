int main(void)
{
	char a[20] = "abc123";
	char *b = a;
	char * c = b+3;
	printf("%s", c);
}
