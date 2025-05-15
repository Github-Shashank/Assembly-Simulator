## Assembler & Hardware Simulation Instructions

### **Overview**
This project contains two main Python files:
1. **Assembler.py**: Used for writing assembly code and converting it into machine code.
2. **HardwareSimulation.py**: Executes the machine code, simulating the program's behavior.

### **Steps to Use**

1. **Open Assembler.py**
   - A tkinter window will open where you can write your assembly code.

2. **Write Assembly Code**
   - Below are the instructions you can use to write assembly code in the Assembler window:

   **Instructions:**
   - **NOP (17)**: A no-operation instruction that does nothing.
   - **HLT (17)**: Halts the program.
   - **<arithmetic_opr> <Rn1> <Rn2> <Rn3> (5,4,4,4)**: Performs arithmetic operations like ADD, SUB, XOR, OR, AND, MUL between registers Rn1 and Rn2, and saves the result to Rn3.
   - **<Rn> (4)**: Represents the 16 registers (R0 to R15).
   - **S_OPR <s_opcodes> <Rn1> <Rn3> (5,4,4,4)**: Executes single operations on Rn1 (like `<<1`, `>>1`, `++1`, `--1`, etc.), saving the result to Rn3.
   - **CMP <cmp_opcodes> <Rn1> <Rn2> (5,4,4,4)**: Compares values in Rn1 and Rn2, saving the result internally to a Boolean variable for use in jump operations.
   - **LDI <Rn1> <0b8> (5,4,8)**: Loads an 8-bit binary value into register Rn1.
   - **LD_M2R/LD_R2M <Rn1> <memory_address> (5,4,8)**: Loads or stores data between memory and registers.
   - **JUMP <type of jump> <address of instruction> (5,2,10)**: Performs a jump to another instruction (useful for loops and conditional statements).
   - **CALL <address of instruction> (7,10)**: Calls a function and saves the current instruction address to the stack.
   - **RET (17)**: Returns from a function call by popping the address from the stack.
   - **INP <Rn1>**: Takes an input number and stores it in register Rn1.
   - **OUT <Rn1>**: Outputs the value of register Rn1.
   - **<s.label1>**: Sets the address of `label1` to a specific line.
   - **<.label1>**: Jumps to the line where `s.label1` is located.

3. **Generate Machine Code**
   - After writing the assembly code, click on "Print text" or "Print machine code."
   - The machine code will be displayed. Copy this machine code into the instruction memory list in **HardwareSimulation.py** (remove commas at the end).

4. **Run HardwareSimulation.py**
   - Run the Python file **HardwareSimulation.py** to simulate the execution of the program with the provided machine code.

### **Example Program**

**Assembly Code:**

```assembly
INP R1
INP R2
CMP = R1 R2 s.cmp
JUMP IF .hlt
CMP < R1 R2
JUMP IF_NOT .r2_g
S_OPR R++ R1 R1
OUT R1
JUMP ONLY .cmp
S_OPR R++ R2 R2 s.r2_g
OUT R2
JUMP ONLY .cmp
HLT s.hlt
```

**Generated Machine Code:**

```plaintext
'01110000000000001','01110000000000010','01001000100010010','01101010000001100',
'01001001100010010','01101100000001001','01000011100010001','01110010000000001',
'01101000000000010','01000011100100010','01110010000000010','01101000000000010',
'00000000000000001',
```

**Execution Output:**
```plaintext
Enter number :- 5
Enter number :- 10
6
7
8
9
10
```

This program takes two numbers as input and increments the smaller number until both numbers are equal.
