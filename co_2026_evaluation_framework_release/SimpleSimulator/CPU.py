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
        rd=self.getBits(word,11,7)
        funct3 =self.getBits(word,14,12)
        rs1 =self.getBits(word,19,15)
        imm =self.sext(self.getBits(word, 31, 20), 12)
        return rd,funct3,rs1,imm
       
    def decodeS(self,word):
        funct3= self.getBits(word,14,12)
        rs1= self.getBits(word,19,15)
        rs2= self.getBits(word,24,20)
        iu= self.getBits(word,31,25)
        il= self.getBits(word,11,7)
        i1= iu<<5
        i2= i1 | il
        i3= self.sext(i2,12)
        imm = i3
        return funct3, rs1, rs2, imm

    def decodeB(self,word):
        funct3= self.getBits(word,14,12)
        rs1= self.getBits(word,19,15)
        rs2= self.getBits(word,24,20)
        i12 = (word>>31) & 1
        i11 = (word>>7) & 1
        i41= self.getBits(word,11,8)
        i105= self.getBits(word,30,25)
        i1= i12<<12
        i2= i11<<11
        i3= i41<<1
        i4= i105<<5
        final=i1|i2|i3|i4
        imm= self.sext(final,13)
        return funct3, rs1, rs2, imm
        

    def decodeU(self,word): #shessaa will do
        rd =self.getBits(word,11,7)
        imm=self.getBits(word,31,12)<<12
        return rd,imm

    def decodeJ(self,word): #shessaa will do
        rd =self.getBits(word,11, 7)
        imm20=self.getBits(word,31,31)
        imm101=self.getBits(word,30,21)
        imm11=self.getBits(word,20,20)
        imm1912=self.getBits(word,19,12)
        imm=self.sext((imm20<<20)|(imm1912<<12)|(imm11<<11)|(imm101<<1),21)
        return rd,imm

    def step(self):
        idx = (self.pc >> 2) + 1
        if self.pc % 4 != 0:
            raise SimulatorError(idx, f"Instruction address misaligned: 0x{self.pc:08X}")
        try:
            word = self.mem.fetchInstr(self.pc)
        except SimulatorError as e:
            raise SimulatorError(idx, f"Invalid instruction fetch: {e.message}")
        opcode=self.getBits(word,6,0)
        nextPc=self.pc+4
        
        if opcode==0b0110011: 
            rd,funct3,rs1,rs2,funct7=self.decodeR(word)
            a=self.sext(self.rf.read(rs1),32)
            b=self.sext(self.rf.read(rs2),32)
            ua=self.rf.read(rs1)
            ub=self.rf.read(rs2)
            shamt=ub & 0x1F
            if funct3==0b000 and funct7==0b0000000: 
                result=a+b
            elif funct3==0b000 and funct7==0b0100000: 
                result=a-b
            elif funct3==0b001 and funct7==0b0000000:
                result=a<<shamt
            elif funct3==0b010 and funct7==0b0000000:
                result=1 if a<b else 0
            elif funct3==0b011 and funct7==0b0000000:
                result=1 if ua<ub else 0
            elif funct3==0b100 and funct7==0b0000000:
                result=a^b
            elif funct3==0b101 and funct7==0b0000000:
                result=ua>>shamt
            elif funct3==0b101 and funct7==0b0100000:
                result=a>>shamt
            elif funct3==0b110 and funct7==0b0000000:
                result=a | b
            elif funct3==0b111 and funct7==0b0000000:
                result=a & b
            else: 
                raise SimulatorError(idx,f"Unknown R-type funct3={funct3} funct7={funct7}")
            self.rf.write(rd,result)

        elif opcode==0b0000011: 
            rd,funct3,rs1,imm=self.decodeI(word)
            addr=(self.rf.read(rs1)+imm) & 0xFFFFFFFF
            try:
                if funct3==0b000:
                    result=self.sext(self.mem.readByte(addr),8)
                elif funct3==0b001:
                    result=self.sext(self.mem.readHalf(addr),16)
                elif funct3==0b010:
                    result=self.mem.readWord(addr)
                elif funct3==0b100:
                    result=self.mem.readByte(addr)
                elif funct3==0b101:
                    result=self.mem.readHalf(addr)
                else: 
                    raise SimulatorError(idx,f"Unknown load funct3={funct3}")
            except SimulatorError as e:
                raise SimulatorError(idx, f"Invalid memory access: {e.message}")
            self.rf.write(rd,result)

        elif opcode==0b0010011: 
            rd,funct3,rs1,imm=self.decodeI(word)
            a =self.sext(self.rf.read(rs1),32)
            ua=self.rf.read(rs1)
            shamt=imm & 0x1F
            funct7=self.getBits(word,31,25)
            if funct3==0b000: 
                result=a+imm
            elif funct3==0b010: 
                result=1 if a<imm else 0
            elif funct3==0b011:
                result=1 if ua<(imm & 0xFFFFFFFF) else 0
            elif funct3==0b100:
                result=a^imm
            elif funct3==0b110:
                result=a | imm
            elif funct3==0b111:
                result=a & imm
            elif funct3==0b001 and funct7==0b0000000:
                result=a<<shamt
            elif funct3==0b101 and funct7==0b0000000:
                result=ua>>shamt
            elif funct3==0b101 and funct7==0b0100000:
                result=a>>shamt
            else: 
                raise SimulatorError(idx,f"Unknown I-ALU funct3={funct3}")
            self.rf.write(rd,result)

        elif opcode==0b1100111: 
            rd,funct3,rs1,imm=self.decodeI(word)
            retAddr=self.pc+4
            target=(self.rf.read(rs1)+imm) & 0xFFFFFFFC
            self.rf.write(rd,retAddr)
            nextPc=target & 0xFFFFFFFF

        elif opcode==0b0100011:
            funct3,rs1,rs2,imm=self.decodeS(word)
            addr=(self.rf.read(rs1)+imm) & 0xFFFFFFFF
            val=self.rf.read(rs2)

            try:
                if funct3==0b000: 
                    base= addr & 0xFFFFFFFC
                    old =self.mem.readWord(base)
                    shift=(addr & 3) * 8
                    mask=0xFF << shift
                    new=(old & ~mask) | ((val & 0xFF) << shift)
                    self.mem.write(base,new)
                elif funct3==0b001:
                    base=addr & 0xFFFFFFFC
                    old =self.mem.readWord(base)
                    shift=(addr & 2)*8
                    mask= 0xFFFF<<shift
                    new=(old & ~mask)|((val & 0xFFFF) << shift)
                    self.mem.write(base,new)
                elif funct3==0b010:
                    self.mem.write(addr,val)
                else:
                    raise SimulatorError(idx,f"Unknown store funct3={funct3}")
            except SimulatorError as e:
                raise SimulatorError(idx, f"Invalid memory access: {e.message}")

        elif opcode==0b1100011:
            funct3,rs1,rs2,imm=self.decodeB(word)
            if funct3==0b000 and rs1==0 and rs2==0 and imm==0:
                return False
            a=self.rf.read(rs1)
            b=self.rf.read(rs2)
            if a & 0x80000000:
                a-=0x100000000
            if b & 0x80000000:
                b-= 0x100000000
            ua= self.rf.read(rs1)
            ub= self.rf.read(rs2)
            if funct3==0b000:
                key=a==b
            elif funct3==0b001:
                key=a!=b
            elif funct3==0b101:
                key=a>=b
            elif funct3==0b100:
                key=a<b
            elif funct3==0b111:
                key=ua>=ub
            elif funct3==0b110:
                key=ua<ub
            else:
                raise SimulatorError(idx,f"Unknown branch funct3={funct3}")
            if key==True:
                nextPc=(self.pc+imm)&0xFFFFFFFF
        elif opcode==0b0110111:
            rd,imm=self.decodeU(word)
            self.rf.write(rd,imm)
        elif opcode==0b0010111:
            rd,imm=self.decodeU(word)
            self.rf.write(rd,self.pc+imm)
        elif opcode==0b1101111:
            rd,imm=self.decodeJ(word)
            self.rf.write(rd,self.pc+4)
            nextPc=(self.pc+imm) & 0xFFFFFFFF
        else:
            raise SimulatorError(idx,f"Unknown opcode: 0b{opcode:07b}")

        if nextPc % 4 != 0:
            raise SimulatorError(idx, f"PC misaligned: 0x{nextPc:08X}")
            

        self.pc=nextPc
        return True

    def traceLine(self):
        pcBin  =f"0b{format(self.pc,'032b')}"
        regBins=' '.join(f"0b{format(r,'032b')}" for r in self.rf.dump())
        return f"{pcBin} {regBins}"
