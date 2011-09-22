;----------------------------------------------------------------------------
; hello.asm complete program
;
; from <http://www.csee.umbc.edu/help/nasm/nasm.shtml>
; 2009-11-18
;
;  The nasm source code is hello.asm
;  This demonstrates basic text output to a screen.
;
;  hello.asm  a first program for nasm for Linux, Intel, gcc
;
; 32-bit (i386) ---
;       assemble:       nasm  -f elf32  -l hello.lst  hello.asm
;       link:           ld   -m elf_i386  -o hello  hello.o
;         or:           gcc  -o hello  hello.o  (only on 32-bit installations)
;
; 64-bit (x86-64/amd64) ---
;       assemble:       nasm  -f elf64  -l hello.lst  hello.asm
;       link:           ld   -m elf_x86_64  -o hello  hello.o
;         or:           gcc  -o hello  hello.o  (only on 64-bit installations)
;
; run:         hello
; output is:    Hello World
;----------------------------------------------------------------------------
        SECTION .data           ; data section
msg:    db "Hello World",10     ; the string to print, 10=cr
len:    equ $-msg               ; "$" means "here"
                                ; len is a value, not an address

        SECTION .text           ; code section
        global main             ; make label available to linker as invoked by gcc
        global _start           ; make label available to linker w/ default entry
main:                           ; standard  gcc  entry point
_start:
       
        mov     edx,len         ; arg3, length of string to print
        mov     ecx,msg         ; arg2, pointer to string
        mov     ebx,1           ; arg1, where to write, screen
        mov     eax,4           ; write command to int 80 hex
        int     0x80            ; interrupt 80 hex, call kernel
       
        mov     ebx,0           ; exit code, 0=normal
        mov     eax,1           ; exit command to kernel
        int     0x80            ; interrupt 80 hex, call kernel
;---------------------------------------------------------------------------- 
