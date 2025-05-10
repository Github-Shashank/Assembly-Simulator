import tkinter as tk
import tkinter.font as tkFont
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

program = 0

mnemonic = {
    'NOP':'0'*17,
    'HLT':'0'*16+'1',
    'ADD':'00010',
    'SUB':'00011',
    'XOR':'00100',
    'OR':'00101',
    'AND':'00110',
    'MUL':'00111',
    'S_OPR':'01000',
    'CMP':'01001',
    'LDI':'01010',
    'LD_M2R':'01011',
    'LD_R2M':'01100',
    'JUMP':'01101',
    'CALL':'1000000',
    'RET':'10000010000000000',

    'SET_0':'0000',
    'RSH':'0001',
    'LSH':'0010',
    'RCL':'0011',
    'LCL':'0100',
    'NOT':'0101',
    'MUL_8-15':'0110',
    'R++':'0111',
    'R--':'1000',
    'NEG':'1001',
    'ODD':'1010',
    'MSB':'1011',
    'LSB':'1100',
    'LEN':'1101',

    'FLAG':'0000',
    '=':'0001',
    '!=':'0010',
    '<':'0011',
    '=>':'0100',
    '>':'0101',
    '=<':'0110',
    'ODD':'0111',
    'EVEN':'1000',

    'R0':'0000',
    'R1':'0001',
    'R2':'0010',
    'R3':'0011',
    'R4':'0100',
    'R5':'0101',
    'R6':'0110',
    'R7':'0111',
    'R8':'1000',
    'R9':'1001',
    'R10':'1010',
    'R11':'1011',
    'R12':'1100',
    'R13':'1101',
    'R14':'1110',
    'R15':'1111',

    'ONLY':'00',
    'IF':'01',
    'IF_NOT':'10',
    'BY':'11',

    'INP':'0111000000000',
    'OUT':'0111001000000'
}

def print_text():
    global program
    """
    This function retrieves the text from the text box
    and prints it to the console.  It gets the entire
    content from the first character ("1.0") to the end ("end").
    """
    program += 1
    print('\nProgram',program,'\n')
    text_content = text_box.get("1.0", "end")
    print("Assembly Code:- \n")
    print(text_content[:-1])
    
    lines = text_content.split('\n')
    code = []
    ins_address_list = []
    for ins_addr, line in enumerate(lines):
        a = ''
        words = line.split(' ')
        for word in words:
            if words == ['']:
                None
            elif word in mnemonic:
                a+=mnemonic[word]
            elif word.isdigit() :
                a+= bin(eval(word+'+256'))[-8:]
            else:
                if word[0:2] == 's.':
                    mnemonic[word[1:]] = bin(ins_addr+1024)[-10:]
                elif word[0] == '.':
                    ins_address_list.append(ins_addr)
                    a+=' '+word
        code.append(a)
    for i in ins_address_list:
        a = ''
        words = code[i].split(' ')
        code[i] = words[0]+mnemonic[words[1]]
        
    print('Machine code :-\n')
    for i in code:
        if len(i) == 17:
            print("'"+i,end="',")

    # Optionally, clear the text box after printing
    text_box.delete("1.0", "end")

# Create the main window
window = tk.Tk()
window.title("Multi-line Text Box Example")  # Set the title of the window

# Create the text box (Text widget)
text_box = tk.Text(window, height=20, width=50)  # Set height and width
text_box.pack(pady=20, padx=20) # Add padding around the textbox

# Create the button to print the text
print_button = tk.Button(window, text="Print Text", command=print_text)
print_button.pack() # Use pack layout

# Create an Exit button
exit_button = tk.Button(window, text="Exit", command=window.destroy)
exit_button.pack(pady=10)

# Start the Tkinter event loop.  This is necessary for the GUI
# to respond to events like button clicks and text entry.
window.mainloop()
