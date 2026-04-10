progMemStart =0x00000000
progMemEnd =0x000000FF
stackMemStart =0x00000100
stackMemEnd=0x0000017F
dataMemStart=0x00010000
dataMemEnd=0x0001007F


class SimulatorError(Exception):
    def __init__(self,lineno,message):
        self.lineno=lineno
        self.message=message
        super().__init__(f"Line {lineno}: {message}")


class Memory: 
    def __init__(self,binaryLines):
        self.imem=[]
        for i,line in enumerate(binaryLines):
            line=line.strip()
            if not line:
                continue
            if len(line)!=32 or any(c not in '01' for c in line):
                raise SimulatorError(i+1,f"Invalid binary line: '{line}'")
            self.imem.append(int(line,2))
        self.dmem={}
        self.smem={}

    def fetchInstr(self,pc):
        idx=(pc-progMemStart)>>2
        if idx<0 or idx>=len(self.imem):
            raise SimulatorError(0,f"PC 0x{pc:08X} out of instruction memory")
        return self.imem[idx]

    def read(self,addr):
        addr &= 0xFFFFFFFF
        if addr%4!=0:
            raise SimulatorError(0,f"Memory read misaligned: 0x{addr:08X}")
        if stackMemStart<=addr<=stackMemEnd:
            return self.smem.get(addr,0)
        if dataMemStart<=addr<=dataMemEnd:
            return self.dmem.get(addr,0)
        raise SimulatorError(0,f"Memory read out of range: 0x{addr:08X}")

    def write(self,addr,value):
        addr &= 0xFFFFFFFF
        value &= 0xFFFFFFFF
        if addr%4!=0:
            raise SimulatorError(0,f"Memory write misaligned: 0x{addr:08X}")
        if stackMemStart<=addr<=stackMemEnd:
            self.smem[addr]=value
        elif dataMemStart<=addr<=dataMemEnd:
            self.dmem[addr]=value
        else:
            raise SimulatorError(0,f"Memory write out of range: 0x{addr:08X}")

    def readWord(self, addr):
        return self.read(addr)

    def readByte(self, addr):
        word=self.read(addr & 0xFFFFFFFC)
        return (word>>((addr & 3)*8)) & 0xFF
    
    def readHalf(self, addr):
        word=self.read(addr & 0xFFFFFFFE)
        return (word>>((addr&2)*8))& 0xFFFF
    
    def dumpData(self):
        lines=[]
        for i in range(32):
            addr=dataMemStart+(i*4)
            val =self.dmem.get(addr,0)
            lines.append(f"0x{addr:08X}:0b{format(val & 0xFFFFFFFF,'032b')}")
        return lines
