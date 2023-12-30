class Disassembler:
  # Constructor
  def __init__(self):
    self.PC = 0
    self.sysHalt = False
    self.register = {}
    self.dataMemory = {}
    self.visitedDataMem = []
    self.instr_dict = {} # map PC : instr
    self.instrHex_dict = {} # map PC : instr in hex code
    self.statistic = {'ALU' : 0, 'Branch' : 0, 'Memory' : 0, 'Other' : 0}
    self.__initMemory()

  # Private: Initialize Register File and Data Memory
  def __initMemory(self):
    for i in range(4):
      self.register[i] = 0
    for i in range(64):
      self.dataMemory[i] = 0
    self.visitedDataMem.clear()
    self.sysHalt = False
    for stat in self.statistic:
      self.statistic[stat] = 0
    return

  # Public: set all data memories to Zero, and PC = 0
  def reset(self):
    self.__initMemory()
    self.PC = 0
    print('Reset Complete')
    print()
    return

  # Public: Read program file prog.asm
  def readProgram(self, fileName):
    # Reading in asm file (prog.asm) into a list of strings
    f = open(fileName)
    lines = f.readlines()
    f.close()
    #############
    print('Loading instruction into dictionary...')
    print()
    # Get rid of of linebreaks
    for i in range(len(lines)):
      lines[i] = lines[i].replace("\n", "")
    # Load instruction into instr_dict
    self.__loadInstrDict(lines)
    return

  # Public: Print all instruction
  def printInstructions(self):
    address = 'address'
    code = 'assembly instruction'
    print('-'*32)
    print(f'|{address:7} : {code:8}|')
    print('|'+'-'*8 + ':' + '-'*21 + '|')
    for line in self.instr_dict:
      print(f'|{line:^7} : ', end = '')
      ins = self.instr_dict[line].split()
      if ins[0] in {'lw', 'sw', 'spar'}:
        instruction = f'{ins[0]} {ins[1]} {ins[3]}({ins[2]})'
        print(f'{instruction:16}    |')
      else:
        print(f'{self.instr_dict[line]:16}    |')
    print('-'*32)
    return

  # Public: Run the line of code of which PC point to
  def runOnce(self):
    endInstr = list(self.instr_dict)[-1]
    if (self.PC > endInstr or self.sysHalt):
      print('Program has reached the end, press \'r\' to reset program, or \'q\' to quit.')
      print()
      return
    else:
      increment = self.__operateInstr(self.PC)
      self.__printDetails(self.PC, increment)
    # increment
    self.PC += increment
    return

  # Public: Run the program to finishing
  def runAll(self):
    print("Running all instruction:... ")
    endInstr = list(self.instr_dict)[-1]
    # run loop to the end of the instruction
    while ((not self.sysHalt) and self.PC < endInstr + 1):
      #if self.PC == 22:
        #print("Hello");
      increment = self.__operateInstr(self.PC)
      self.PC += increment
    print()


  # Private: operate instruction store in line,
  # and return the increment for updating PC
  def __operateInstr(self, PC):
    line = self.instr_dict[PC]
    # Halt
    if (line == 'Halt'):
      self.sysHalt = True;
      return 0;
    instruction = line.replace("$", "").split()
    opCode = instruction[0]
    # Jump type
    try:
      imm = int(instruction[1])
    except:
      print(f'Error at opCode = {opCode}')
    if opCode == 'jmp':
      return self.__jmp(imm)
    # Branch type
    try:
      rt = int(instruction[1])
      imm = int(instruction[2])
    except:
      print(f'Error at opCode = {opCode}')
    if opCode == 'bez':
      return self.__bez(rt, imm)
    # I-type
    try:
      rt = int(instruction[1])
      rs = int(instruction[2])
      imm = int(instruction[3])
    except:
      print(f'Error at opCode = {opCode}')
    if opCode == 'addi':
      return self.__addi(rt, rs, imm)
    elif opCode == 'andi':
      return self.__andi(rt, rs, imm)
    elif opCode == 'lw':
      return self.__lw(rt, rs, imm)
    elif opCode == 'sw':
      return self.__sw(rt, rs, imm)
    elif opCode == 'slli':
      return self.__slli(rt, rs, imm);
    elif opCode == 'comp':
      return self.__comp(rt, rs, imm);
    try:
      return # Error if reach this line
    except:
      print('Instruction not found')

  # Private: operate 'addi'
  def __addi(self, rt, rs, imm):
    self.register[rt] = self.register[rs] + imm
    self.statistic['ALU'] += 1
    return 1

  # Private: operate 'andi'
  def __andi(self, rt, rs, imm):
    self.register[rt] = self.register[rs] & imm
    self.statistic['ALU'] += 1
    return 1

  # PrivateL: operate 'slli'
  def __slli(self, rt, rs, imm):
    if (imm > 0):
      self.register[rt] = self.register[rs] << imm
    else:
      if (self.register[rt] < 0):
        self.register[rt] = self.register[rt] + pow(2, 16)
      imm = imm * (-1);
      result = self.register[rs] >> imm
      self.register[rt] = result
    self.statistic['ALU'] += 1
    return 1;

  # Private: operate 'comp'
  def __comp(self, rt, rs, imm):
    if (imm == 0):
      self.register[rt] = ~(self.register[rs])
    else:
      self.register[rt] = ~(self.register[rs]) + 1
    self.statistic['ALU'] += 1
    return 1;
    
  # Private: operate 'bez'
  def __bez(self, rt, imm):
    # print(f'beq r{rt} = {self.register[rt]}')
    # print(f'imm = {imm}')
    self.statistic['Branch'] += 1
    if self.register[rt] == 0:
      return imm
    else:
      return 1

  # Private: operate 'lw'
  def __lw(self, rt, rs, imm):
    address = self.register[rs] + imm
    self.register[rt] = self.dataMemory[address]
    self.statistic['Memory'] += 1
    return 1

  # Private: operate 'sw'
  def __sw(self, rt, rs, imm):
    address = self.register[rs] + imm
    self.dataMemory[address] = self.register[rt]
    self.visitedDataMem.append(address)
    self.statistic['Memory'] += 1
    return 1

  def __jmp(self, imm):
    self.statistic['Branch'] += 1
    return imm;

  # Private: print details of instruction execution
  def __printDetails(self, PC, PCincrement):
    print('-'*35)
    line = self.instr_dict[PC]
    inst = line.replace("$", "").split()
    print(f' Machine code: 0x{self.instrHex_dict[PC]}')
    if inst[0] in {'lw', 'sw'}:
      print(f' Assembly code: {inst[0]} ${inst[1]} {inst[3]}(${inst[2]})')
    else:
      print(f' Assembly code: {line}')
    if inst[0] == 'jmp':
      print(f'  |imm = {inst[1]}')
    elif inst[0] == 'bez':
      print(f'  |rt = ${inst[1]}')
      print(f'  |imm = {inst[2]}')
    # I-type
    else:
      print(f'  |rt = ${inst[1]}')
      print(f'  |rs = ${inst[2]}')
      print(f'  |imm = {inst[3]}')
    if inst[0] not in {'bez', 'sw', 'jmp'}:
       print(f' update ${inst[1]} = {self.register[int(inst[1])]}')
    if inst[0] in {'sw'}:
       address = self.register[int(inst[2])] + int(inst[3])
       print(f' update M[{address}] = {self.register[int(inst[1])]}')
    print(f' update PC = {PC + PCincrement}')
    print('-'*35)
    return

  # Public: print datas from all register and data memory
  # Print Register File and Data Memory
  def printRFDM(self):
    # print all registers
    numRow = 5
    self.__printNiceFormatRegister(self.register, numRow)
    # print all Data Memories
    numCol = 4
    self.__printNiceFormatDataMem(self.visitedDataMem, numCol)
    print()
    print(f'Program Counter PC = {self.PC}')
    print('-'*51)
    print()
    return

  # Public: for printing instruction statistic
  def printStats(self):
    print('-'*20)
    print('Instruction Statistics: ')
    sumStat = 0
    for stat, data in self.statistic.items():
      print(f' |{stat}: {data}')
      sumStat += data
    print(f'Total: {sumStat}')
    print('-'*20)
    print()
    return
    
  # Private: for printing out register in a nice format
  def __printNiceFormatRegister(self, dict, numRow):
    print('-'*51)
    print('Register File:')
    j = 0;
    while j < numRow:
      i = j
      while i < len(dict):
        print(f'${i:<2} = {dict[i]:<4}', end = ' | ')
        i += numRow
      print()
      j += 1
    print('-'*51)
    return

  # Private: for printing out register in a nice format
  def __printNiceFormatDataMem(self, dataList, numCol):
    duplicate = {} #
    for key in self.dataMemory: # prevent duplicate printing of data memory
      duplicate[key] = 0 #
    print('Memory Data:')
    newLine = 0
    for address in sorted(dataList):
      if duplicate[address] == 0:
        print(f'M[{address:2}] = {self.dataMemory[address]:<3}', end = ' | ')
        duplicate[address] += 1
        if newLine == numCol - 1:
          print()
          newLine = 0
        else:
          newLine += 1
    print()
    if len(dataList) == 0:
      print('No Data Memory was used. All Data Memories contain value of 0')
    else:
      print('All other Data Memories are unused and contain value of 0')
    print('-'*51)
    return

  # Private: Converting hex code to instruction
  def __loadInstrDict(self, lines):
    Pcounter = 0
    for i in range(len(lines)):
      self.instrHex_dict[Pcounter] = lines[i]
      biCode = bin(int(lines[i], base=16))[2:].zfill(8)
      if biCode[0] == '0' or biCode[1] == '1':
        self.__Itype(biCode, Pcounter)
      elif biCode[0] == '1':
        self.__Btype(biCode, Pcounter)
      Pcounter += 1
    return
    
  # Private: Identify I-type instruction
  def __Itype(self, biCode, address):
    rt = int(biCode[3:5], base=2)
    rs = int(biCode[5:7], base=2)
    op = ''
    # addi
    if biCode[:3] == '000':
      op = 'addi'
      if biCode[5] == '0':
        rs = 1
      else:
        rs = 3
      immArr = [-1, 0, 1, 2]
      index = int(biCode[6:], base=2)
      imm = immArr[index]
    # andi
    elif biCode[:3] == '001':
      op = 'andi'
      imm = int(biCode[7], base=2)
    # lw
    elif biCode[:3] == '111':
      op = 'lw'
      if biCode[7] == '0':
        imm = 0
      else:
        imm = 32
    # sw
    elif biCode[:3] == '110':
      op = 'sw'
      if biCode[7] == '0':
        imm = 0
      else:
        imm = 32
    # slli
    elif biCode[:3] == '010':
      op = 'slli'
      if biCode[7] == '0':
        imm = 4
      else:
        imm = -1
    # comp
    elif biCode[:3] == '011':
      op = 'comp'
      imm = int(biCode[7], base=2)
    # combine op rt rs imm for instruction
    self.instr_dict[address] = f'{op} ${rt} ${rs} {imm}'
    return

  # Private: Identify J-type instruction
  def __Btype(self, biCode, address):
    op = ''
    rt = ''
    if biCode == '10100000':
      self.instr_dict[address] = f'Halt'
    elif biCode[:3] == '100':
      op = 'bez'
      rt = int(biCode[3:5], base=2)
      imm = int(biCode[5:], base=2)
      self.instr_dict[address] = f'{op} ${rt} {imm}'
    elif biCode[:3] == '101':
      op = 'jmp'
      imm = int(biCode[3:], base=2)
      if biCode[3] == '1':
        imm = imm - 0b100000
      self.instr_dict[address] = f'{op} {imm}'
    return

def userInput():
  inp = ''
  inp += '#\n' 
  inp += '# Enter \'s\' for Step Run, \'n\' for Non-stop Run,\n'
  inp += '# \'v\' to view data, \'r\' to reset program,\n'
  inp += '# \'i\' for instruction count, or \'q\' to quit: '
  return inp

### main ###
def main():
  prog = Disassembler()
  file = input("Enter file name: ")
  prog.readProgram(file)
  prog.printInstructions()
  cin = ''
  while (cin != 'q'):
    cin = input(userInput())
    print('#')
    if (cin == 's'):
      prog.runOnce()
    elif (cin == 'n'):
      prog.runAll()
      prog.printRFDM()
      prog.printStats()
    elif (cin == 'v'):
      prog.printRFDM()
    elif (cin == 'r'):
      prog.reset()
    elif (cin == 'i'):
      prog.printStats()
  print('Bye!')
  return

main()