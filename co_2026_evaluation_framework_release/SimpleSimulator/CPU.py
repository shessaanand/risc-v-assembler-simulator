# Fetch-decode-execute. 
#CPU.py uses memory.py and registerfile.py

# step() returns False on virtual halt, True otherwise.

from memory import SimulatorError
from registerfile import RegisterFile


class CPU:

    def __init__(self,mem):
        self.mem=mem
        self.rf =RegisterFile()
        self.pc =0x00000000

    def sext(self,value,bits):
        if value & (1<<(bits-1)):
            value -= (1<<bits)
        return value

    def getBits(self,word,hi,lo):
        mask=(1<<(hi-lo+1))-1
        return (word>>lo) & mask

    def decodeR(self,word): #sang will do
        rd = self.getBits(word,11,7)
        funct3 = self.getBits(word,14,12)
        rs1 = self.getBits(word,19,15)
        rs2 = self.getBits(word,24,20)
        funct7 = self.getBits(word,31,25)
        return rd,funct3,rs1,rs2,funct7

    def decodeI(self,word): #sang will do
       rd = self.getBits(word,11,7)
       funct3 = self.getBits(word,14,12)
       rs1 = self.getBits(word,19,15)
       imm = self.sext(self.getBits(word,31,20),12)
       return rd,funct3,rs1,imm
       
    def decodeS(self,word): #sujeet will do
        

    def decodeB(self,word): #sujeet will do
        

    def decodeU(self,word): #shessaa will do
        rd =self.getBits(word,11, 7)
        imm=self.sext(self.getBits(word,31,12),20)<<12
        return rd,imm

    def decodeJ(self,word): #shessaa will do
        rd =self.getBits(word,11, 7)
        imm20=self.getBits(word,31,31)
        imm101=self.getBits(word,30,21)
        imm11=self.getBits(word,20,20)
        imm1912=self.getBits(word,19,12)
        imm=self.sext((imm20<<20)|(imm1912<<12)|(imm11<<11)|(imm101<<1),21)
        return rd,imm

    def step(self): #shessaa will do
        word =self.mem.fetchInstr(self.pc)
        opcode=self.getBits(word,6,0)
        nextPc=self.pc+4
        idx=(self.pc>>2)+1
        
        # R-type  opcode 0110011
        if opcode==0b0110011: 
            rd,funct3,rs1,rs2,funct7=self.decodeR(word)
            a =self.sext(self.rf.read(rs1),32)
            b=self.sext(self.rf.read(rs2),32)
            ua =self.rf.read(rs1)
            ub=self.rf.read(rs2)
            shamt=ub & 0x1F
            if funct3==0b000 and funct7==0b0000000: 
                result=a+b
            elif funct3==0b000 and funct7==0b0100000: 
                result=a-b
            elif #...
                result=#...
            elif #...
                result=#...
            elif #...
                result=#...
            elif #...
                result=#...
            elif #...
                result=#...
            elif #...
                result=#...
            elif #...
                result=#...
            else: 
                raise SimulatorError(idx,f"Unknown R-type funct3={funct3} funct7={funct7}")
            self.rf.write(rd,result)

        # I-type loads  opcode 0000011
        elif opcode==0b0000011: 
            rd,funct3,rs1,imm=self.decodeI(word)
            addr=(self.rf.read(rs1)+imm) & 0xFFFFFFFF
            if #...
                #...
            else: 
                raise SimulatorError(idx,f"Unknown load funct3={funct3}")

        # I-type ALU  opcode 0010011
        elif opcode==0b0010011: 
            rd,funct3,rs1,imm=self.decodeI(word)
            a =self.sext(self.rf.read(rs1),32)
            ua=self.rf.read(rs1)
            if #... 
                result=#...
            elif #...: 
                result=#...
            else: 
                raise SimulatorError(idx,f"Unknown I-ALU funct3={funct3}")
            self.rf.write(rd,result)

        # jalr  opcode 1100111
        elif opcode==0b1100111: 
            rd,funct3,rs1,imm=self.decodeI(word)
            retAddr=#...
            target =#...
            self.rf.write(rd,retAddr)
            nextPc =#...

        # S-type  opcode 0100011
        elif opcode==0b0100011: 
            funct3,rs1,rs2,imm=self.decodeS(word)
            addr=(self.rf.read(rs1)+imm) & 0xFFFFFFFF
            if #...:
                #...
            else: 
                raise SimulatorError(idx,f"Unknown store funct3={funct3}")

        # B-type  opcode 1100011
        elif opcode==0b1100011: 
            funct3,rs1,rs2,imm=self.decodeB(word)
            a =self.sext(self.rf.read(rs1),32)
            b =self.sext(self.rf.read(rs2),32)
            ua=self.rf.read(rs1)
            ub=self.rf.read(rs2)
            if #...:
                taken=#...  
            if   #... 
               taken=#...
            elif #...: 
                taken=#...
            elif #...: 
                taken=#...
            elif #... 
                taken=#...
            elif #...
                taken=#...
            elif #... 
               taken=#...
            else: 
                raise SimulatorError(idx,f"Unknown branch funct3={funct3}")
            if taken:
                #...

        # U-type LUI  opcode 0110111
        elif opcode==0b0110111:
            rd,imm=self.decodeU(word)
            self.rf.write(rd,imm)

        # U-type AUIPC  opcode 0010111
        elif opcode==0b0010111:
            rd,imm=self.decodeU(word)
            self.rf.write(rd,self.pc+imm)

        # J-type JAL  opcode 1101111
        elif opcode==0b1101111:
            rd,imm=self.decodeJ(word)
            self.rf.write(rd,self.pc+4)
            nextPc=(self.pc+imm) & 0xFFFFFFFF

        else:
            raise SimulatorError(idx,f"Unknown opcode: 0b{opcode:07b}")

        self.pc=nextPc
        return True

    def traceLine(self):
        pcBin  =f"0b{format(self.pc,'032b')}"
        regBins=' '.join(f"0b{format(r,'032b')}" for r in self.rf.dump())
        return f"{pcBin} {regBins} "
