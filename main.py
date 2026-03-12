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

def compute_machine_code(command_list):
    # convert each command list like [addi, x1, x2, 3] to  machine code (hex string) and return hex_string
    return 

if __name__ == "__main__":
    main()
