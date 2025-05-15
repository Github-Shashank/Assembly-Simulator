import tkinter as tk
import tkinter.font as tkFont
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
import re

program = 0
current_indent = 0.0
if_id = 0
if_indent = {}
while_id = 0
while_indent = {}
for_id = 0
for_indent = {}
def_id = 0
def_indent = {}
indent_code = {}
variable = {}
d = {
    '+':'ADD',
    '-':'SUB',
    '^':'XOR',
    '|':'OR',
    '&':'AND',
    '*':'MUL'
    }

def mem_addr_var(var):
    if not var in variable:
        variable[var] = str(len(variable))
        return variable[var]
    else:
        print('Already initialised')

def int_var(s):
    pattern = r"^int\s+([a-zA-Z_][a-zA-Z0-9_]*)$"
    match = re.match(pattern,s)
    if match:
        var1 = match.group(1)
        mem_addr_var(var1)
    return re.match(pattern, s) is not None    

def set_var(s):
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(\d+)$" # a = 5
    match = re.match(pattern,s)
    if match:
        var1 = match.group(1)
        var2 = match.group(2)
        a = f'''LDI R0 {var2}
LD_R2M R0 {variable[var1]}'''
        print(a)
    return re.match(pattern, s) is not None

def get_var(s):
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)$"
    match = re.match(pattern,s)   # a = b
    if match:
        var1 = match.group(1)
        var2 = match.group(2)
        a = f'''LD_M2R R0 {variable[var2]}
LD_R2M R0 {variable[var1]}'''
        print(a)
    return re.match(pattern, s) is not None

def input_var(s):
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*input\(\)$"
    match = re.match(pattern,s)
    if match:                   # a = input()
        var1 = match.group(1)
        a = f'''INP R0
LD_R2M R0 {variable[var1]}'''
        print(a)
    return re.match(pattern, s) is not None

def print_var(s):
    pattern = r"^print\(([a-zA-Z_][a-zA-Z0-9_]*)\)$"
    match = re.match(pattern,s)
    if match:                   # print(a)
        var1 = match.group(1)
        a = f'''LD_M2R R0 {variable[var1]}
OUT R0'''
        print(a)
    return re.match(pattern, s) is not None

def setexp_var(s):
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([-+*/^|&]?)\s*([a-zA-Z_][a-zA-Z0-9_]*)$"    
    match = re.match(pattern,s)
    if match:                   # a = b + c
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        var4 = match.group(4)      
        a = f'''LD_M2R R0 {variable[var2]}
LD_M2R R1 {variable[var4]}
{d[var3]} R0 R1 R2
LD_R2M R2 {variable[var1]}'''
        print(a)
    return re.match(pattern, s) is not None

def updatexp_byvar(s):
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*([-+*/^|&])=\s*([a-zA-Z_][a-zA-Z0-9_]*)$"
    match = re.match(pattern,s)
    if match:                   # a += b
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        a = f'''LD_M2R R0 {variable[var1]}
LD_M2R R1 {variable[var3]}
{d[var2]} R0 R1 R0
LD_R2M R0 {variable[var1]}'''
        print(a)
    return re.match(pattern, s) is not None

def updatexp_var(s):
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*([-+*/^|&])=\s*(\d+)$"
    match = re.match(pattern,s)
    if match:                   # a += 5
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        a = f'''LDI R0 {var3}
LD_M2R R1 {variable[var1]}
{d[var2]} R1 R0 R1
LD_R2M R1 {variable[var1]}'''
        print(a)
    return re.match(pattern, s) is not None

def singleopr_var(s):
    possible_values = [
      re.escape('to 0'),
      re.escape('>>1'),
      re.escape('<<1'),
      re.escape('<<cl'),
      re.escape('>>cl'),
      re.escape('~'),
      re.escape('mul'),
      re.escape('++1'), # + needs escaping
      re.escape('--1'), # - inside [] needs escaping, but here it's fine, though escaping is safer
      re.escape('&1'),
      re.escape('&10000000'),
      re.escape('length')
    ]
    values_pattern = "|".join(possible_values)
    pattern = re.compile(rf"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*({values_pattern})$")
    match = re.match(pattern,s)
    if match:                   # a =b>>1
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        a = f'''LD_M2R R0 {variable[var1]}
LD_M2R R1 {variable[var2]}
S_OPR {var3} R1 R0
LD_R2M R0 {variable[var1]}'''
        print(a)
    return pattern.match(s) is not None

def if_line(s):
    global current_indent
    global if_id
    operators = [
      re.escape('=='),
      re.escape('!='),
      re.escape('<'),
      re.escape('=>'),
      re.escape('>'),
      re.escape('=<'),
      re.escape('odd'),
      re.escape('even')
    ]
    operators_pattern = "|".join(operators)
    pattern = re.compile(rf"^if\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*({operators_pattern})\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:$")
    match = re.match(pattern,s)
    if match:                   # if a == b:
        if_id += 1
        if_indent[current_indent] = f"{if_id}_{int(current_indent)}"
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        a = f'''LD_M2R R0 {variable[var1]}
LD_M2R R1 {variable[var3]}
CMP {var2} R0 R1
JUMP IF_NOT .else_{if_indent[current_indent]}'''
        print(a)
    return pattern.match(s) is not None

def else_line(s):
    global current_indent
    pattern = r"^else\s*:$"
    match = re.match(pattern,s)
    if match:
        indent_code[current_indent] = f'''NOP s.end_if_{if_indent[current_indent]}'''
        a = f'''JUMP ONLY .end_if_{if_indent[current_indent]}
NOP s.else_{if_indent[current_indent]}'''
        print(a)
    return re.match(pattern, s) is not None

def while_line(s):
    global current_indent
    global while_id
    operators = [
      re.escape('=='),
      re.escape('!='),
      re.escape('<'),
      re.escape('=>'),
      re.escape('>'),
      re.escape('=<'),
      re.escape('odd'),
      re.escape('even')
    ]
    operators_pattern = "|".join(operators)
    pattern = re.compile(rf"^while\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*({operators_pattern})\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:$")
    match = re.match(pattern,s)
    if match:                   # while a==b:
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        while_id += 1
        while_indent[current_indent] = f"{while_id}_{int(current_indent)}"
        indent_code[current_indent] = f'''JUMP ONLY .while_{while_indent[current_indent]}
NOP s.whlie_not_{while_indent[current_indent]}'''
        a = f'''NOP s.while_{while_indent[current_indent]}
LD_M2R R15 {variable[var1]}
LD_M2R R14 {variable[var3]}
CMP {var2} R15 R14
JUMP IF_NOT .whlie_not_{while_indent[current_indent]}'''
        print(a)
    return pattern.match(s) is not None

def for_line(s):
    global current_indent
    global for_id
    pattern = re.compile(r"^for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+range\(\s*(\d+)\s*\)\s*:$")
    match = re.match(pattern,s)
    if match:                   # for i in range(40):
        var1 = match.group(1)
        var2 = match.group(2)
        for_id += 1
        for_indent[current_indent] = f"{for_id}_{int(current_indent)}"
        indent_code[current_indent] = f'''LD_M2R R13 {variable[var1]}
S_OPR R++ R13 R13
LD_R2M R13 {variable[var1]}
JUMP ONLY .for_{for_indent[current_indent]}
NOP s.if_for_{for_indent[current_indent]}'''
        a = f'''LD_M2R R13 {variable[var1]}
NOP s.for_{for_indent[current_indent]}
LDI R12 {var2}
CMP >= R13 R12
JUMP IF .if_for_{for_indent[current_indent]}'''
        print(a)
    return pattern.match(s) is not None

def define(s):
    global current_indent
    global def_id
    pattern = re.compile(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*:$")
    match = re.match(pattern, s)
    if match:
        function_name = match.group(1)
        if function_name not in ['print','input']:
            def_id += 1
            def_indent[current_indent] = f"{def_id}_{int(current_indent)}"
            indent_code[current_indent] = f'''RET
NOP s.skip_{def_indent[current_indent]}'''
            arguments_str = match.group(2)
            arguments = [arg.strip() for arg in arguments_str.split(',') if arg.strip()]

            a = f'''JUMP ONLY .skip_{def_indent[current_indent]}
NOP s.func_{function_name}'''
            print(a)
            for i in arguments:
                int_var(f'int {i}')
            for i,var in enumerate(arguments):
                print(f'LD_R2M R{i} {variable[var]}')
                
            return pattern.match(s) is not None
    return False

def function(s):
  pattern = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)$")
  match = re.match(pattern, s)

  if match:
    function_name = match.group(1)
    if function_name not in ['print','input']:
        arguments_str = match.group(2)
        arguments = [arg.strip() for arg in arguments_str.split(',') if arg.strip()]
        for i,var in enumerate(arguments):
            print(f'LD_M2R R{i} {variable[var]}')
        print(f'CALL .func_{function_name}')
        return pattern.match(s) is not None
    return False


def indent(s,i=4):
    global current_indent
    n = (len(s)-len(s.lstrip()))/i
    if n==int(n):
        current_indent = n
        return True
    else:
        print("Indentation Error")
        return False

def indent_remain():
    global current_indent
    d = []
    for i in indent_code:
        if i >= current_indent:
            print(indent_code[i])
            d.append(i)
    for i in d:
        del indent_code[i]


def print_text():
    global program
    global current_indent
    """
    This function retrieves the text from the text box
    and prints it to the console.  It gets the entire
    content from the first character ("1.0") to the end ("end").
    """
    program += 1
    print('\nProgram',program,'\n')
    text_content = text_box.get("1.0", "end")

    print(text_content)
    l = text_content.split('\n')
    print()
    for i in l:
        if indent(i):
            indent_remain()
            s = i.strip()
            int_var(s)
            set_var(s)
            get_var(s)
            input_var(s)
            print_var(s)
            setexp_var(s)
            updatexp_var(s)
            updatexp_byvar(s)
            singleopr_var(s)
            if_line(s)
            else_line(s)
            while_line(s)
            for_line(s)
            define(s)
            function(s)
    current_indent = 0
    indent_remain()
    print('HLT')        
    
    # Optionally, clear the text box after printing
    text_box.delete("1.0", "end")

# Create the main window
window = tk.Tk()
window.title("Multi-line Text Box Example")  # Set the title of the window

# Create the text box (Text widget)
text_box = tk.Text(window, height=20, width=50)  # Set height and width
text_box.pack(pady=20, padx=20) # Add padding around the textbox

# Create the button to print the text
print_button = tk.Button(window, text="Print Assembly Code", command=print_text)
print_button.pack() # Use pack layout

# Create an Exit button
exit_button = tk.Button(window, text="Exit", command=window.destroy)
exit_button.pack(pady=10)

# Start the Tkinter event loop.  This is necessary for the GUI
# to respond to events like button clicks and text entry.
window.mainloop()
