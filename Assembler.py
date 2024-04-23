# Define the opcodes and function codes for MIPS instructions
opcodes = {
    'add': '000000', 'sub': '000000', 'lw': '100011', 'sw': '101011',
    'beq': '000100', 'bne': '000101', 'slt': '000000', 'addu': '000000',
    'addiu': '001001', 'lui': '001111', 'ori': '001101', 'jal': '000011', 'jr': '000000', 'addi': '001000','j': '000010'
}

func_codes = {
    'add': '100000', 'sub': '100010', 'slt': '101010', 'addu': '100001', 'jr': '001000'
}

# Define register codes for MIPS registers
reg_codes = {
    '$zero': '00000', '$t1': '01001', '$t2': '01010', '$t3': '01011', '$t4': '01100',
    '$t5': '01101', '$t6': '01110', '$t7': '01111', '$t8': '11000', '$t9': '10001',
    '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111', '$v0': '00010',
    '$a0': '00100', '$ra': '11111', '$1': '00001'
}
num={'0': '0000', '1': '0001','2': '0010','3':'0011','4': '0100','5': '0101','6': '0110','7': '0111','8':'1000','9':'1001'}
label={'loop2': 4194396, 'loop3': 4194412, 'loop4': 4194496}
# Initialize an empty list to store the generated machine code
machine_code = []
# Initialize a dictionary to store labels and their corresponding addresses
label_dict = {}
label_beq=[]
# Function to assemble R-type instructions
def assemble_r_type(parts):
    return opcodes[parts[0]] + reg_codes[parts[2]] + reg_codes[parts[3]] + reg_codes[parts[1]] + '00000' + func_codes[parts[0]]
# Function to assemble I-type instructions
def assemble_i_type(parts):
    if(parts[0]=='bne'):
        return opcodes[parts[0]] + reg_codes[parts[2]] + reg_codes[parts[1]] + '000000000000'+ num[str(label_dict[parts[3]]-1)]
    if(parts[0]=='addi'):
        return opcodes[parts[0]] + reg_codes[parts[2]] + reg_codes[parts[1]] + '000000000000'+ num[parts[3]]
    if(parts[0]=='beq'):
        if(parts[3]=='loop2end'):
            return opcodes[parts[0]] + reg_codes[parts[1]] + reg_codes[parts[2]] + '{0:016b}'.format(label_dict[parts[3]]-2)
        else:
            return opcodes[parts[0]] + reg_codes[parts[1]] + reg_codes[parts[2]] + '{0:016b}'.format(label_dict[parts[3]]-1)
def assemble_lw_sw_type(parts):
    k=parts[2].index('$')
    l=parts[2].index(')')
    o=parts[2].index('(')
    return opcodes[parts[0]] + reg_codes[parts[2][k:l]] + reg_codes[parts[1]] + '000000000000' + num[parts[2][:o]]
# Function to assemble J-type instructions
def assemble_j_type(parts):
    return opcodes[parts[0]] + '00000'+ bin(label[parts[1]])[2:-2]
# Function to process each line of assembly code
def process_line(line,lineno,pass_no):
    # Remove comments and whitespace
    line = line.split("#")[0].strip()
    # Skip empty lines
    if not line:
        return
    # Split the line into parts (operation and operands)
    line=line.replace(',',' ')
    parts = line.split()
    # Handle labels (only in the first pass)
    if ((parts[0] in ['bgt','beq']) and pass_no==1):
        label2=parts[3]
        label_beq.append(parts[3])
        label_dict[label2]=lineno
    if ((":" in line) and pass_no==1):
        label3 = parts[0][:-1]
        if(label3 in label_dict):
            label_dict[label3] = lineno-label_dict[label3]
        return
    # Skip to the next iteration if it's the first pass
    if pass_no == 1:
        return 
    # Assemble R-type instructions
    if parts[0] in ['add', 'sub', 'slt', 'addu', 'jr']:
        machine_code.append(assemble_r_type(parts))
    # Assemble I-type instructions
    elif parts[0]=='subi':
        machine_code.append(assemble_i_type(['addi','$1','$zero',parts[3]]))
        machine_code.append(assemble_r_type(['sub',parts[1],parts[2],'$1']))
    elif parts[0] in ['lw','sw']:
        machine_code.append(assemble_lw_sw_type(parts))
    elif parts[0] in ['bne', 'addiu', 'lui', 'ori','addi']:
        machine_code.append(assemble_i_type(parts))
    # Assemble J-type instructions
    elif parts[0] in ['jal','j']:
        machine_code.append(assemble_j_type(parts))
    # Assemble custom 'move' instruction
    elif parts[0] == 'move':
        machine_code.append(assemble_r_type(['addu', parts[1], '$zero', parts[2]]))
    # Assemble custom 'bgt' instruction
    elif parts[0] == 'bgt':
        machine_code.append(assemble_r_type(['slt', '$1', parts[2], parts[1]]))
        machine_code.append(assemble_i_type(['bne', '$zero', '$1', parts[3]]))
    elif parts[0] == 'beq':
        machine_code.append(assemble_i_type(parts))
# First pass to collect labels
with open("mips.txt", 'r') as infile:
    lineno=0
    for line in infile:
        if ':' not in line:
            lineno+=1
        for key in label_beq:
            if key in line:
                lineno+=1
        process_line(line,lineno,1)

# Second pass to generate machine code
machine_code.clear()
with open("mips.txt", 'r') as infile, open('machine_code.txt', 'w') as outfile:
    lineno=0
    for line in infile:
        lineno+=1
        process_line(line,lineno,2)
    # Write the machine code to the output file
    for code in machine_code:
        outfile.write(code + '\n')
