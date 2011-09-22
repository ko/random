        SECTION .text           ; code section
        global main             ; make label available to linker as invoked by gcc
        global _start           ; make label available to linker w/ default entry
main:                           ; standard  gcc  entry point
_start:
	jmp short ender
	
	starter:

	xor eax,eax		; clean up registers
	xor ebx,ebx
	xor ecx,ecx
	xor edx,edx

	mov al, 4		; syscall for write
	mov bl, 1		; stdout
	pop ecx			; tricky pop
	mov dl, 5		; length of string
	int 0x80		; enter kernel mode

	exit:
	xor eax,eax		; clean up registers
	mov al, 1		; exit
	xor ebx,ebx		; clean up registers or exit status 0
	int 0x80		; enter kernel mode

	ender:
	call starter		; put the address of the string on the stack
	db 'hello'
