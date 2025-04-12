section .data
    num dd 0

global _procesarNumero
section .text

;to compile: nasm -f elf32 procesarNumero.asm
_procesarNumero:
    push ebp
    mov ebp,esp

    fld dword [ebp + 8] 

    fistp dword [num]

    mov eax, [num]
    add eax, 1
    mov [num], eax

    mov esp, ebp 
    pop ebp
    ret