import time

# Program Counter

program_counter = -1
program_counter_bin = '00000000000000000'
steps_counter = -1
jump = False

# Memory

ins_memory = [
               '01110000000000001','01110000000000010','01001000100010010','01101010000001100','01001001100010010','01101100000001001','01000011100010001','01110010000000001','01101000000000010','01000011100100010','01110010000000010','01101000000000010','00000000000000001'
              ]
rom = {'00000000':'00000000' ,'00000001':'00000000' ,'00000010':'00000000' ,'00000011':'00000000' ,'00000100':'00000000' ,'00000101':'00000000' ,'00000110':'00000000' ,'00000111':'00000000' ,'00001000':'00000000' ,'00001001':'00000000' ,'00001010':'00000000' ,'00001011':'00000000' ,'00001100':'00000000' ,'00001101':'00000000' ,'00001110':'00000000' ,'00001111':'00000000' ,'00010000':'00000000' ,'00010001':'00000000' ,'00010010':'00000000' ,'00010011':'00000000' ,'00010100':'00000000' ,'00010101':'00000000' ,'00010110':'00000000' ,'00010111':'00000000' ,'00011000':'00000000' ,'00011001':'00000000' ,'00011010':'00000000' ,'00011011':'00000000' ,'00011100':'00000000' ,'00011101':'00000000' ,'00011110':'00000000' ,'00011111':'00000000' ,'00100000':'00000000' ,'00100001':'00000000' ,'00100010':'00000000' ,'00100011':'00000000' ,'00100100':'00000000' ,'00100101':'00000000' ,'00100110':'00000000' ,'00100111':'00000000' ,'00101000':'00000000' ,'00101001':'00000000' ,'00101010':'00000000' ,'00101011':'00000000' ,'00101100':'00000000' ,'00101101':'00000000' ,'00101110':'00000000' ,'00101111':'00000000' ,'00110000':'00000000' ,'00110001':'00000000' ,'00110010':'00000000' ,'00110011':'00000000' ,'00110100':'00000000' ,'00110101':'00000000' ,'00110110':'00000000' ,'00110111':'00000000' ,'00111000':'00000000' ,'00111001':'00000000' ,'00111010':'00000000' ,'00111011':'00000000' ,'00111100':'00000000' ,'00111101':'00000000' ,'00111110':'00000000' ,'00111111':'00000000' ,'01000000':'00000000' ,'01000001':'00000000' ,'01000010':'00000000' ,'01000011':'00000000' ,'01000100':'00000000' ,'01000101':'00000000' ,'01000110':'00000000' ,'01000111':'00000000' ,'01001000':'00000000' ,'01001001':'00000000' ,'01001010':'00000000' ,'01001011':'00000000' ,'01001100':'00000000' ,'01001101':'00000000' ,'01001110':'00000000' ,'01001111':'00000000' ,'01010000':'00000000' ,'01010001':'00000000' ,'01010010':'00000000' ,'01010011':'00000000' ,'01010100':'00000000' ,'01010101':'00000000' ,'01010110':'00000000' ,'01010111':'00000000' ,'01011000':'00000000' ,'01011001':'00000000' ,'01011010':'00000000' ,'01011011':'00000000' ,'01011100':'00000000' ,'01011101':'00000000' ,'01011110':'00000000' ,'01011111':'00000000' ,'01100000':'00000000' ,'01100001':'00000000' ,'01100010':'00000000' ,'01100011':'00000000' ,'01100100':'00000000' ,'01100101':'00000000' ,'01100110':'00000000' ,'01100111':'00000000' ,'01101000':'00000000' ,'01101001':'00000000' ,'01101010':'00000000' ,'01101011':'00000000' ,'01101100':'00000000' ,'01101101':'00000000' ,'01101110':'00000000' ,'01101111':'00000000' ,'01110000':'00000000' ,'01110001':'00000000' ,'01110010':'00000000' ,'01110011':'00000000' ,'01110100':'00000000' ,'01110101':'00000000' ,'01110110':'00000000' ,'01110111':'00000000' ,'01111000':'00000000' ,'01111001':'00000000' ,'01111010':'00000000' ,'01111011':'00000000' ,'01111100':'00000000' ,'01111101':'00000000' ,'01111110':'00000000' ,'01111111':'00000000'}
reg = {'0000':'00000000' ,'0001':'00000000' ,'0010':'00000000' ,'0011':'00000000' ,'0100':'00000000' ,'0101':'00000000' ,'0110':'00000000' ,'0111':'00000000' ,'1000':'00000000' ,'1001':'00000000' ,'1010':'00000000' ,'1011':'00000000' ,'1100':'00000000' ,'1101':'00000000' ,'1110':'00000000' ,'1111':'00000000'}

# Specially stored

mul = '00000000'
boolean = False

# ALU

alu = {
    '00010': lambda a, b: a + b,        # Addition
    '00011': lambda a, b: a - b,        # Subtraction
    '00100': lambda a, b: a ^ b,        # XOR
    '00101': lambda a, b: a | b,        # OR
    '00110': lambda a, b: a & b,        # AND
    '00111': lambda a, b: a * b,        # Multiplication
}

s_alu = {
    '0000': lambda x: '0',                      # Clear to 0
    '0001': lambda x: x[2:]+'0',                # Logical Right Shift
    '0010': lambda x: '0'+x[:-1],               # Logical Left Shift
    '0011': lambda x: x[-1]+x[:-1],             # Right Shift by clock
    '0100': lambda x: x[1:]+x[0],               # Left Shift by clock
    '0101': lambda x: x.replace('0','2').replace('1','0').replace('2','1'),  # Bitwise NOT
    '0110': lambda x: mul,                      # Loads special register mul which applied earlier
    '0111': lambda x: bin(int(x,2)+1)[2:],      # Increment
    '1000': lambda x: bin(int(x,2)-1)[2:],      # Decrement
    '1001': lambda x: '11111111',               # Negate
    '1010': lambda x: x[-1],                    # Odd check (returns 1 if odd, 0 if even)
    '1011': lambda x: x[0],                     # MSB (Most Significant Bit)
    '1100': lambda x: x[-1],                    # LSB (Least Significant Bit)
    '1101': lambda x: bin(len(bin(x)[2:])),     # Bit length (ignoring '0b')
    # '1110' and '1111' not defined
}

cmp = {
    '0000': lambda a, b: False,       # Undefined, or NOP
    '0001': lambda a, b: a == b,      # Equal
    '0010': lambda a, b: a != b,      # Not equal
    '0011': lambda a, b: a < b,       # Less than
    '0100': lambda a, b: a >= b,      # Greater than or equal
    '0101': lambda a, b: a > b,       # Greater than
    '0110': lambda a, b: a <= b,      # Less than or equal
    '0111': lambda a, b: (a - b) & 0b1 == 1,  # Odd (least significant bit is 1)
    '1000': lambda a, b: (a - b) & 0b1 == 0,  # Even (least significant bit is 0)
}#,'1001':'' ,'1010':'' ,'1011':'' ,'1100':'' ,'1101':'' ,'1110':'' ,'1111':''}

# Jump

jmp = {'00':'no_condition','01':'if boolean','10':'if not boolean','11':'increment ins address by'}
cal = {'00':'call','01':'return'}#,'10':'','11':''}

# Stack

stack = []

def check_ins_code(s):
    if s.count('0') + s.count('1') != 17:
        print('Memory Length Error')
        return False
    return True

def oopcode_path(s):
    s = s or '00000000000000000'
    
    if not check_ins_code(s):
        return

    oopcode = s[:5]
    
    if oopcode == '00000':
        print()
        
    elif oopcode in ['01101','01111','10000','10001']:
        insdrive_address_path(s)
        
    elif oopcode in ['01010','01011','01100']:
        mem_address_path(s)
        
    elif oopcode == '01110':
        suboopcode = s[5:7]
        
        if suboopcode == '00':
            a = input('Enter number :- ')
            reg[s[13:17]] = bin(eval(a+'+256'))[-8:]
            
        elif suboopcode == '01':
            print(int(reg[s[13:17]],2)) # Output
            
    else :
        alu_address_path(s)

def mem_address_path(s):
    oopcode = s[:5]
    addr = s[5:9]
    value = s[9:]

    if oopcode == '01011':
        reg[addr] = rom[value]  # Load value from rom to reg
    elif oopcode == '01100':
        rom[value] = reg[addr]  # Store value from reg to rom
    else:
        reg[addr] = value  # Direct assignment to reg

def alu_process(r1, o, r2, r12):
    global mul
    a = int(reg[r1], 2)
    b = int(reg[r2], 2)

    if o in alu:
        result = alu[o](a, b)
        reg[r12] = bin(result + (1 << 8))[-8:]

        # Overflow detection (if result doesn't match 8-bit value)
        if result != int(reg[r12], 2):
            mul = bin(result + (1 << 8))[-16:-8]

def salu_process(r2, s_oopcode, r12):
    if s_oopcode in s_alu:
        reg[r12] = format(s_alu[s_oopcode](reg[r2]),'08b')
    else:
        reg[r12] = '11110000'

def salu_process(r2, s_oopcode, r12):
    if s_oopcode in s_alu:
        func = s_alu[s_oopcode]
        if s_oopcode in ['0000', '0011', '0100', '0101']:  # operate directly on binary strings
            reg[r12] = func(reg[r2])
        else:
            reg[r12] = format(func(int(reg[r2], 2)), '08b')
    else:
        reg[r12] = '11110000'

def cmp_process(r1, o, r2):
    global boolean
    val1 = int(reg[r1], 2)
    val2 = int(reg[r2], 2)

    if o in cmp:
        boolean = cmp[o](val1, val2)

def alu_address_path(s):
    global program_counter, jump, boolean
    oopcode = s[:5]
    addr1 = s[5:9]
    addr2 = s[9:13]
    addr3 = s[13:17]

    if oopcode in ['00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001']:
        if oopcode == '01000':
            salu_process(addr2, addr1, addr3)
        elif oopcode == '01001':
            cmp_process(addr2, addr1, addr3)
        else:
            alu_process(addr1, oopcode, addr2, addr3)
            
def jump_process(s):
    global program_counter_bin, program_counter, jump
    path = s[5:7]
    jump_address = s[7:]
    
    if path == '00' or (path == '01' and boolean) or (path == '10' and not boolean):
        program_counter_bin = jump_address
        jump = True
    elif path == '11':
        sum_val = int(jump_address, 2) + program_counter
        program_counter_bin = bin(sum_val)[2:]
        jump = True



def stack_process(s):
    global program_counter_bin, program_counter, jump
    path = s[5:7]
    
    if path == '00':
        # Push next instruction address to stack and jump
        stack.append(format(program_counter + 1, '017b'))  # Assuming 17-bit program counter
        program_counter_bin = s[7:]
        jump = True

    elif path == '01':
        # Return from stack to previous address
        if stack:
            program_counter_bin = stack.pop()
            jump = True
        else:
            print("Stack Underflow: No return address available")

def insdrive_address_path(s):
    oopcode = s[:5]
    if oopcode == '01101':         # JUMP
        jump_process(s)
    elif oopcode == '10000':       # CALL / RETURN
        stack_process(s)

# Program Counter

while True:
    # Execute instruction based on jump flag
    if jump:
        jump = False
        program_counter = int(program_counter_bin, 2)
    else:
        program_counter += 1

    # Fetch and execute instruction
    instruction = ins_memory[program_counter]
    oopcode_path(instruction)

    # Safety limiter to prevent infinite loops
    steps_counter += 1
    if steps_counter > 100:
        confirm = input("Program exceeded 100 steps. Continue? (True/False): ")
        if not eval(confirm):
            break

    # Halt conditions
    if instruction == '00000000000000000':
        time.sleep(100)  # Simulate infinite loop (NOP or HALT)
    elif instruction == '00000000000000001':
        break  # HALT
