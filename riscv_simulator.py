running = True #boolean loop
registers = {'x0':0,'x1':0,'x2':0,'x3':0,'x4':0,'x5':0,'x6':0,'x7':0,'x8':0,'x9':0,'x10':0,'x11':0,'x12':0,'x13':0,'x14':0,'x15':0,'x16':0,'x17':0,'x18':0,'x19':0,'x20':0,'x21':0,'x22':0,'x23':0,'x24':0,'x25':0,'x26':0,'x27':0,'x28':0,'x29':0,'x30':0,'x31':0,'x32 ':0,}
instruction_details = {'add':['0110011','000','0000000'],'sub':['0110011','000','0100000'],'xor':['0110011','100','0000000'],'or':['0110011','110','0000000'],'and':['0110011','111','0000000'],'sll':['0110011','001','0000000'],'srl':['0110011','101','0000000'],'sra':['0110011','101','0100000'],'slt':['0110011','010','0000000'],'sltu':['0110011','011','0000000'] #R-TYPE
          ,'addi':['0010011','000',''],'xori':['0010011','100',''],'ori':['0010011','110',''],'andi':['0010011','111',''],'slli':['0010011','001','0000000'],'srli':['0010011','101','0000000'],'srai':['0010011','101','0100000'],'slti':['0010011','010',''],'sltiu':['0010011','011',''] #I-TYPE (NORMAL)
          ,'lb':['0000011','000',''],'lh':['0000011','001',''],'lw':['0000011','010',''],'lbu':['0000011','100',''],'lhu':['0000011','101',''] #I-TYPE (LOAD)
          ,'sb':['0100011','000',''],'sh':['0100011','001',''],'sw':['0100011','010',''] #S-TYPE
          ,'beq':['1100011','000',''],'bne':['1100011','001',''],'blt':['1100011','100',''],'bge':['1100011','101',''],'bltu':['1100011','110',''],'bgeu':['1100011','111',''],} #B-TYPE
#instruction_details are listed, respectively, as OPCODE,FUNC3,FUNC7

#TODO : Add more opcodes (J-TYPE,U-TYPE and some other instructions)

def check_instruction(exec):
    try:
        instruction = exec.split(' ') #fetch instruction
        targets = instruction[1].split(',') #return target registers
        instruction = instruction[0] #'real' instruction
        details = instruction_details[instruction] #get instruction details
        targets_binary = [(bin(int(x.strip('x'))).strip('ob')) for x in targets] #return binary target
        #targets are listed, respectively, as RD,RS1,RS2
        return [instruction,details,targets_binary,targets]
    except:
        return '0'

def target_to_binary(target,utility_len): #leading zeros
    target = target.lstrip('0b')
    ans = "".join(['0'] * (utility_len-len(target))) + target
    return ans

def instruction_to_hex(instruction):
    opcode = str(instruction[1][0])
    funct3 = str(instruction[1][1])
    funct7 = str(instruction[1][2])
    rs1 = str(target_to_binary(instruction[2][1],5)) #2
    rs2 = str(target_to_binary(instruction[2][2],5)) #3
    rd = str(target_to_binary(instruction[2][0],5)) #1
    imm_12 = str(target_to_binary(instruction[2][2],12))
    imm_13 = str(target_to_binary(instruction[2][2],13))
    imm_7_1 = str(imm_12[abs(11-12)-1:abs(5-12)]) #[11:5] (see testes.py for further explaining)
    imm_7_2 = str(imm_13[12] + imm_13[abs(10-13)-1:abs(5-13)]) #[12] + [10:5]
    imm_5_1 = str(imm_12[abs(4-13)-1::]) #[4:0]
    imm_5_2 = str(imm_13[abs(4-13)-1:abs(1-13)] + imm_13[11] )#[4:1] + [11]
    if opcode == '0110011': #R-TYPE
        binary_instruction = [funct7+rs2+rs1+funct3+rd+opcode]
        final_targets = [rd,rs1,rs2]
    elif opcode == '0010011' or opcode == '0000011': #I-TYPE
        binary_instruction = [imm_12+rs1+funct3+rd+opcode]
        final_targets = [rd,rs1,imm_12]        
    elif opcode == '0100011': #S-TYPE
        binary_instruction = [imm_7_1+rs2+rs1+funct3+imm_5_1+opcode]
        final_targets = [imm_7_1+imm_5_1,rs1,rs2]
    elif opcode == '1100011': #B-TYPE
        binary_instruction = [imm_7_2+rs2+rs1+funct3+imm_5_2+opcode]
        final_targets = [imm_7_2+imm_5_2,rs1,rs2]
    print(binary_instruction)
    hexb = hex(int(binary_instruction[0],2))
    return [str(hexb).upper(),instruction,final_targets]

def execute_instruction(instruction,targets):
    opcode = str(instruction[0])
    func3 = str(instruction[1])
    if opcode == '0110011': #R-TYPE
        func7 = str(instruction[2])
        rd = targets[0]
        rs1 = targets[1]
        rs2 = targets[2]
        if func3 == '000': #ADD e SUB
            if func7 == '0000000': #ADD
                registers[rd] = int(registers[rs1] + registers[rs2])
            else: #SUB
                registers[rd] = int(registers[rs1] - registers[rs2])
        #restantes
    elif opcode == '0010011': #I-TYPE
        pass
    elif opcode == '0000011': #I-TYPE LOAD
        pass
    elif opcode == '0100011': #S-TYPE
        pass
    elif opcode == '1100011': #B-TYPE
        pass
#check load and store (how it works)


###### MAIN METHOD ######
while running:
    instruction = input('\nInsira a instrução: \n')
    executable = check_instruction(instruction)
    if executable == '0':
        print('Invalid Instruction. Please try again.')
    print(executable) #debugging
    hexa = instruction_to_hex(executable)
    print(hexa) #debugging
    doit = execute_instruction(hexa[1][1],executable[3])
    prompt = input('\nQuer realizar mais instruções?\n'f"Digite '1' caso queira , ou '0' caso não queira\n")
    print(f"\n{registers}") #print à última atualização dos registos
    if prompt == '0':
        running = False





    
