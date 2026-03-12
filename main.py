import sys

def main():
    # Get filename from command line argument, or use default
    if len(sys.argv) < 2:
        print("input file name")
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

            # get rid of commas space
            line = line.replace(",", "")
            
            # make list of values
            command_list = line.split()
            instructions.append(command_list)
    
    return instructions

def reg_to_bin(reg):
    num = int(reg.replace('x', ' '))
    return format(num, '05b')

def imm_to_bin(imm_str):
    imm = int(imm_str)          
    if imm < 0:                 
        imm = (1 << 12) + imm   # two's complement
    return format(imm, '012b') 

def compute_machine_code(command_list):
    # convert each command list like [addi, x1, x2, 3] to  machine code (hex string) and return hex_string
    instruct = command_list[0]

    if instruct in ["addi", "slli", "srli", "ori", "andi" ]:
        rd = reg_to_bin(command_list[0])
        rs1 = reg_to_bin(command_list[1])
        imm = imm_to_bin(command_list[3])

        opcode = 0b0010011

        funct3_map = {
            "addi":0b000,
            "ori":0b110,
            "andi":0b111,
            "slli":0b001,
            "srli":0b101
        }

        funct3 = funct3_map[instruct]

        if instruct in ["slli","srli"]:
            funct7 = 0b0000000
            shamt = imm 

            machine = (
                (funct7 << 25) |
                (shamt << 20) |
                (rs1 << 15) |
                (funct3 << 12) |
                (rd << 7) |
                opcode
            )

        else:
            imm = imm 

            machine = (
                (imm << 20) |
                (rs1 << 15) |
                (funct3 << 12) |
                (rd << 7) |
                opcode
            )

    return format(machine, 'x')

if __name__ == "__main__":
    main()
