SECTION .text
global _start

_start:
	jmp short   string

	flop:
	pop      esi				; address of "Hello world",10
	xor      eax, eax			; clear registers
	xor      ebx, ebx
	xor      ecx, ecx
	xor      edx, edx
	mov byte       al, 0x4			; 4 is write
	mov byte       bl, 0x1			; 1 is stdout
	lea            ecx, [esi]		; put ecx as memory dump from esi
	mov byte       dl, 0xd
	int            0x80

	xor       eax, eax
	xor      ebx, ebx
	mov byte   al, 0x1
	int      0x80

	string:
	call           flop
	db             'Hello world',10 	; 10 is CR
