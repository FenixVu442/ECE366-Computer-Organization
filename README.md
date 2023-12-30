Name: Manh Vu Bui
Class: ECE366 - Computer Organization
Instructor: Prof. Rao Wenjing
Project: MoonWalk: 16-bit ISA with 8-bit Instructions for the Parity Array Program
Environment: Python, Circuit-Verse

Visualization of Architecture Implementation:
![image](https://github.com/FenixVu442/ECE366-Project-MoonWalk-ISA/assets/104748038/469d0b17-3ad0-4a3b-9aa4-2ead46cabf17)
Link: https://circuitverse.org/users/142873/projects/project-isa_moonwalk

Parity Assembly Program:  par.txt
--------------------------------
|address : assembly instruction|
|--------:---------------------|
|   0    : addi $1 $1 2        |
|   1    : slli $1 $1 4        |
|   2    : addi $1 $1 -1       |
|   3    : addi $2 $1 1        |
|   4    : andi $0 $1 1        |
|   5    : bez $0 2            |
|   6    : comp $2 $2 1        |
|   7    : sw $2 0($1)         |
|   8    : bez $1 2            |
|   9    : jmp -7              |
|  10    : addi $1 $1 2        |
|  11    : slli $1 $1 4        |
|  12    : addi $1 $1 -1       |
|  13    : lw $0 0($1)         |
|  14    : andi $2 $0 1        |
|  15    : bez $2 5            |
|  16    : lw $3 32($1)        |
|  17    : addi $3 $3 1        |
|  18    : andi $3 $3 1        |
|  19    : sw $3 32($1)        |
|  20    : slli $0 $0 -1       |
|  21    : bez $0 2            |
|  22    : jmp -8              |
|  23    : bez $1 2            |
|  24    : jmp -12             |
|  25    : Halt                |
--------------------------------

Enter: "par.txt" to start run the simulation. 
