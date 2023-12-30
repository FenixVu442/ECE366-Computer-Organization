class Disassembler:
  # Constructor
  def __init__(self):
    self.PC = 0
    self.register = {}
    self.dataMemory = {} 
    self.instr_dict = {} # map PC : instr
    self.label_dict = {} # map label : PC
    self.__initMemory()

  # Private: Initialize Register File and Data Memory
  def __initMemory(self):
    for i in range(32):
      self.register[i] = 0
    for i in range(0x2000, 0x21FF):
      self.dataMemory[i] = 0
    return
    
  # Public: Read program file prog.asm
  def readProgram(self, fileName):
    # Reading in asm file (prog.asm) into a list of strings
    f = open(fileName)
    lines = f.readlines()
    f.close()
    #############
    print('Loading instruction and label into dictionaries...')
    # Get rid of of linebreaks
    for i in range(len(lines)):
      lines[i] = lines[i].replace("\n", "")
    # Load instruction into instr_dict
    self.__loadInstrDict(lines)
    return


  # Private: Converting hex code to instruction
  def __loadInstrDict(self, lines):
    Pcounter = 0;
    for ln in lines:
      pos = ln.find(":")
      if pos < 0: # line is an instruction
        self.instr_dict[Pcounter] = ln
        print(f'{ln:20} is an instruction, addr = {Pcounter}')
        Pcounter += 4
      else: # line is a label
        self.label_dict[ln[:pos]] = Pcounter;
        print(f'{ln:20} is a label, point to addr = {Pcounter}')
    print()
    return

  def runAll(self):
    print("Running all instruction:... ")
    endInstr = list(self.instr_dict)[-1]
    # run loop to the end of the instruction
    while (self.PC < endInstr + 4):
      # run instruction at address PC
      self.__operateInstr(self.instr_dict[self.PC])
      self.PC += 4
    print()  
    return


  def __operateInstr(self, line):
    print(f'PC = {self.PC} : {line}')
    instruction = line.split()
    opCode = instruction[0]
    if (opCode == 'addi'):
      self.__addi(instruction)
    elif (opCode == 'slt'):
      self.__slt(instruction)
    elif (opCode == 'beq'):
      self.__beq(instruction)
    return
    
  
  def __addi(self, instruction):
    rt = int(instruction[1].replace("$", "").replace(",", ""))
    rs = int(instruction[2].replace("$", "").replace(",", ""))
    # print(f'  read ${rs} = {self.register[rs]}')
    imm = int(instruction[3])
    # print(f'  read imm = {imm}')

    self.register[rt] = self.register[rs] + imm
    print(f'  write ${rt} = {self.register[rt]}')
    return


  def __slt(self, instruction):
    rd = int(instruction[1].replace("$", "").replace(",", ""))
    rt = int(instruction[2].replace("$", "").replace(",", ""))
    # print(f'  read ${rt} = {self.register[rt]}')
    rs = int(instruction[3].replace("$", ""))
    # print(f'  read ${rs} = {self.register[rs]}')

    if self.register[rt] < self.register[rs]:
      self.register[rd] = 1
    else:
      self.register[rd] = 0

    print(f'  write ${rd} = {self.register[rd]}')
    return

  def __beq(self, instruction):
    rt = int(instruction[1].replace("$", "").replace(",", ""))
    rs = int(instruction[2].replace("$", "").replace(",", ""))
    # print(f'  read ${rs} = {self.register[rs]}')
    imm = int(self.label_dict[instruction[3]])
    # print(f'  read imm = {imm}')

    if (self.register[rs] == self.register[rt]):
      self.PC = imm - 4

    print(f'  update PC = {self.PC + 4}')
    return

  def printRegister(self):
    print('Printing all register: ')
    for i in range(len(self.register)):
      data = self.register[i]
      hexCode = self.__toHex(data)
      print(f'${i:<2} = {self.register[i]} = {hexCode} ')
    print()
    print(f'PC = {self.PC} = {hex(self.PC)}')
    return

  
  def __toHex(self, num):
    num = num & 0xFFFFFFFF
    return hex(num)

#### main ###
prog = Disassembler()
prog.readProgram("Example1.txt")
