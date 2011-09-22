;----------------------------------------------------------------------------
; pause.asm complete program
;
; adapted from <http://www.csee.umbc.edu/help/nasm/nasm.shtml>
; 2011-09-13
;
;  The nasm source code is pause.asm
;  This demonstrates basic text output to a screen.
;
;  pause.asm  a first program for nasm for Linux, Intel, gcc
;
; 64-bit (x86-64/amd64) ---
;       assemble:       nasm  -f elf64  -l pause.lst  pause.asm
;       link:           ld   -m elf_x86_64  -o pause  pause.o
;         or:           gcc  -o pause  pause.o  (only on 64-bit installations)
;
; run:         pause
; output is:   nothing! lol. 
;----------------------------------------------------------------------------
        SECTION .text           ; code section
        global main             ; make label available to linker as invoked by gcc
        global _start           ; make label available to linker w/ default entry
main:                           ; standard  gcc  entry point
_start:
	xor	eax,eax
        mov     al,29           ; pause command to int 80 hex
        int     0x80            ; interrupt 80 hex, call kernel
       
;---------------------------------------------------------------------------- 
