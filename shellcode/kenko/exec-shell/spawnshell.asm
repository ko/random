;----------------------------------------------------------------------------
; spawnshell.asm complete program
;
; int execve(const char *filename, char *const argv[], char *const envp[]); 
; 
; Calling:
;
;	execve ("/bin/sh", "", NULL);
;
; Requirements:
;
;	EAX: 0x11d
;	EBX: "/bin/sh"
;	ECX: Address of argument vector
;	EDX: Address of envrionemnt vector
;
; 64-bit (x86-64/amd64) ---
;
;       assemble:       nasm  -f elf64  -l pause.lst  pause.asm
;       link:           ld   -m elf_x86_64  -o pause  pause.o
;         or:           gcc  -o pause  pause.o  (only on 64-bit installations)
;
;----------------------------------------------------------------------------
        SECTION .text           ; code section
        global main             ; make label available to linker as invoked by gcc
        global _start           ; make label available to linker w/ default entry
main:                           ; standard  gcc  entry point
_start:
	jmp	tricks

	xor	eax,eax
        mov     al,11           ; set eax to 11d (sys_execve)
        int     0x80            ; interrupt 80 hex, call kernel

tricks:
	call	_start		; tricky jump back to _start
	
       
;---------------------------------------------------------------------------- 
