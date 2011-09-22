;;; -*- coding: utf-8; mode: assembler -*-
;;; hello.asm - Hello world in assembler for DOS, Linux i386 and amd64
;;; Copyright © 2008 Göran Weinholt <goran@weinholt.se>

;;; This program is free software: you can redistribute it and/or modify
;;; it under the terms of the GNU General Public License as published by
;;; the Free Software Foundation, either version 3 of the License, or
;;; (at your option) any later version.

;;; This program is distributed in the hope that it will be useful,
;;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;; GNU General Public License for more details.

;;; You should have received a copy of the GNU General Public License
;;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

	section .text
	global _start
	bits 16

;;; I was wondering if it was possible on the Intel x86 to determine
;;; if one was running in 16-bit, 32-bit or 64-bit mode. This is a
;;; program that assembles to the same instruction stream in three
;;; binary formats. When run it prints a message.

;;; The 16-bit binary was tested under FreeDOS. The 32-bit and 64-bit
;;; binaries run on Linux.
	
;;; Build with this line (tested with nasm 2.05.01):

;;; nasm -fbin -o hello16.com hello.asm && nasm -felf64 -o hello64.o hello.asm && ld -o hello64 hello64.o && nasm -felf -o hello32.o hello.asm && ld -m elf_i386 -o hello32 hello32.o


_start:	xor ax,ax		;all zeroes in ax/eax
	not ax			;all ones in ax/eax
	shr ax,16		;shift right 16 bits
	test ax,ax
	jnz short check64	;not zero => more than 16 bits
	jmp short dos

hello16:db 'Hello, 16-bit world!',13,10,'$'
dos:	mov dx,(hello16-_start+0x100)
	mov ah,9
	int 0x21		;print to stdout
	ret

	bits 32
check64:xor eax,eax		;all zeroes in ax/eax
	dec eax
	mov edx,eax		;In 64-bit mode: mov rdx, rax
	test eax,eax
	jz short linux64	;If eax was not decremented...
	jmp short linux32

hello32:db 'Hello, 32-bit world!',10
linux32:call eip
eip:	pop ecx
	mov edx,(linux32-hello32)
	sub ecx,(eip-hello32)
	jmp short exit

hello64:db 'Hello, 64-bit world!',10
linux64:mov edx,(linux64-hello64)
	lea ecx,[hello64-exit]	;same as: [rel hello64] in 64-bit mode
exit:	mov ebx,1		;stdout
	mov eax,4		;sys_write
	int 0x80

	xor ebx,ebx
	mov eax,1		;sys_exit
	int 0x80

