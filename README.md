
## 🧠 Assembly Language Toolkit

This project simulates a simple assembly-like instruction set architecture (ISA), including:

- A **GUI-based Assembler** (`Assembler.py`)  
- A **Python-like Compiler to Assembly** (`Compiler.py`)  
- A **Hardware Simulation Environment** (`Assembly_CLI_Simulation.py`)  

---

## 🔧 Components

### 1. `Compiler.py` — High-Level Python-like Syntax to Assembly
- Write simple Python-style code like:
```python
int a
a = 5
b = input()
a += b
print(a)
```
- Translates into equivalent assembly instructions
- Supports:
  - Variable declarations
  - Arithmetic
  - `if`, `else`, `while`, `for`, `def`, and function calls
  - `input()` / `print()`
- Click **"Print Assembly Code"** to generate and display assembly

### 2. `Assembler.py` — GUI Assembly to Machine Code
- Built with `tkinter`
- Converts your assembly language to machine code
- Features label support and opcode generation
- Click **"Print Machine Code"** to output the code
- Supports instructions like:
  - `NOP`, `HLT`, `ADD`, `SUB`, `XOR`, `MUL`, `LDI`, `JUMP`, `CALL`, `RET`, etc.
  - `INP` / `OUT` for input/output
  - `S_OPR` and `CMP` for single operations and comparisons
  - Label definitions like `s.label1` and references like `.label1`

#### 📋 Example Assembly Input
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

### 3. `Assembly_CLI_Simulation.py` — Hardware Execution Environment
- Simulates memory (`ROM`, `Registers`, `Instruction Memory`)
- Interprets machine code and executes
- Includes support for:
  - ALU operations
  - Single-operand processing
  - Jump/call/return via a stack
  - `INP`, `OUT` instructions
- Automatically tracks steps and halts after 500 steps unless confirmed to continue

---

## 🚀 How to Run

### Step 1: Write Code in High or Low level language
- Use `Compiler.py` to write Python-style code for high level language
- Skip to Step 3 for low level language

### Step 2: Generate Assembly Code
- Click **"Print Assembly Code"**

### Step 3: Write Assembly Code
- Use `Assembler.pu` to write your own assembly code or get from `Compiler.pu`

### Step 4: Write Machine Code
- Paste the machine code into the `ins_memory` array in `Assembly_CLI_Simulation.py`

### Step 5: Run Simulation
```bash
python Assembly_CLI_Simulation.py
```

### Step 6: Observe Output
- Program will ask for integer inputs and also ouput in the range 0 to 255
- At the end, it prints HALT 
---

## 🧪 Sample Output

```plaintext
Enter number :- 5
Enter number :- 10
6
7
8
9
10
```

---

## 📁 File Structure

```
├── Assembler.py
├── Assembly_CLI_Simulation.py
├── Compiler.py
└── README.md  ← (this file)
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
