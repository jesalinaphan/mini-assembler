import sys

def main():
    # Get filename from command line argument, or use default
    if len(sys.argv) < 2:
        print("input file name")
        return
    else:
        filename = sys.argv[1]
    
    instructions = read_assembly_file(filename)

    output_list = []

    for instr in instructions:
        machine_code = compute_machine_code(instr)
        output_list.append(machine_code)
    
    for code in output_list:
        print(code)
    

def read_assembly_file(filename):
    instructions = []
    
    with open(filename, 'r') as f:
        for line in f:
            
            # don't process comments if there are any in the code
            if '#' in line:
                line = line[:line.index('#')]
            
            # skip empty lines
            line = line.strip()
            if not line:
                continue

            # get rid of commas
            line = line.replace(",", "")
            
            # make list of values
            command_list = line.split()
            instructions.append(command_list)
    
    return instructions

def reg_to_bin(reg):
    pseudo_reg = {
        "zero": "x0",
        "ra": "x1",
        "sp": "x2",
        "gp": "x3",
        "tp": "x4",
        "t0": "x5",
        "t1": "x6",
        "t2": "x7",
        "s0": "x8",
        "fp": "x8",
        "s1": "x9",
        "a0": "x10",
        "a1": "x11",
        "a2": "x12",
        "a3": "x13",
        "a4": "x14",
        "a5": "x15",
        "a6": "x16",
        "a7": "x17",
        "s2": "x18",
        "s3": "x19",
        "s4": "x20",
        "s5": "x21",
        "s6": "x22",
        "s7": "x23",
        "s8": "x24",
        "s9": "x25",
        "s10": "x26",
        "s11": "x27",
        "t3": "x28",
        "t4": "x29",
        "t5": "x30",
        "t6": "x31"
    }
    if reg in pseudo_reg:
        reg = pseudo_reg[reg]
    num = int(reg.replace('x', ''))
    return format(num, '05b')

def imm_to_bin(imm_str):
    imm = int(imm_str)          
    if imm < 0:                 
        imm = (1 << 12) + imm   # two's complement
    return format(imm, '012b') 

def shamt_to_bin(shamt_str):
    shamt = int(shamt_str)
    return format(shamt, '05b')

def imm_to_bin_branch(imm_str):
    imm = int(imm_str)
    if imm < 0:                 
        imm = (1 << 13) + imm   # two's complement
    return format(imm, '013b') # 13 bits then drop the lsb    

def compute_machine_code(command_list):
    # convert each command list like [addi, x1, x2, 3] to  machine code (hex string) and return hex_string
    instruct = command_list[0].lower()
    command_list[0] = instruct
    if instruct in ["mul", "add", "sll", "srl", "xor"]:
        machine_code = convert_R_type(command_list)
    elif instruct in ["addi", "slli", "srli", "ori", "andi"]:
        machine_code = convert_I_type(command_list)
    elif instruct in ["beq", "bne"]:
        machine_code = convert_branch_type(command_list)
    else:
        print("Unknown command type")
        return
    return machine_code

def convert_R_type(command_list):
    R_type = {
        "mul": "000",
        "add": "000",
        "sll": "001",
        "srl": "101",
        "xor": "100"
    }

    funct7 = "0000000"
    rs2 = reg_to_bin(command_list[3])
    rs1 = reg_to_bin(command_list[2])
    func3 = R_type[command_list[0]]
    rd = reg_to_bin(command_list[1])
    opcode = "0110011"

    if command_list[0] == "mul":
        funct7 = "0000001"

    binary_str = funct7 + rs2 + rs1 + func3 + rd + opcode
    integer = int(binary_str, 2)
    hex_str = format(integer, '08x')

    return hex_str

def convert_I_type(command_list):
    funct3_map = {
        "addi":"000",
        "ori":"110",
        "andi":"111",
        "slli":"001",
        "srli":"101"
    }

    rd = reg_to_bin(command_list[1])
    rs1 = reg_to_bin(command_list[2])
    opcode = "0010011"
    funct3 = funct3_map[command_list[0]]

    if command_list[0] in ["slli","srli"]:
        imm = shamt_to_bin(command_list[3])
        funct7 = "0000000"
        binary_str = funct7 + imm + rs1 + funct3 + rd + opcode

    else:
        imm = imm_to_bin(command_list[3])
        binary_str = imm + rs1 + funct3 + rd + opcode

    integer = int(binary_str, 2)
    hex_str = format(integer, '08x')

    return hex_str

def convert_branch_type(command_list):
    branch_type = {
        "beq": "000",
        "bne": "001"
    }
    imm = imm_to_bin_branch(command_list[3])
    rs2 = reg_to_bin(command_list[2])
    rs1 = reg_to_bin(command_list[1])
    func3 = branch_type[command_list[0]]
    opcode = "1100011"

    binary_str = imm[0] + imm[2:8] + rs2 + rs1 + func3 + imm[8:12] + imm[1] + opcode
    integer = int(binary_str, 2)
    hex_str = format(integer, '08x')

    return hex_str

if __name__ == "__main__":
    main()
