char shellcode[] =
	"\x31\xc0\xb0\x1d\xcd\x80";

int main(int argc, char **argv)
{
int (*func)();
func = (int (*)()) shellcode;
(int)(*func)();
}
