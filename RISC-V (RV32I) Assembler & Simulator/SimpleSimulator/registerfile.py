stackInitSP=0x0000017C

class RegisterFile:

    def __init__(self):
        self.regs=[0]*32
        self.regs[2]=stackInitSP

    def read(self,idx):
        return self.regs[idx] & 0xFFFFFFFF

    def write(self,idx,value):
        if idx!=0:
            self.regs[idx]=value & 0xFFFFFFFF

    def dump(self):
        result = []
        for i in range(32):
            result.append(self.regs[i] & 0xFFFFFFFF)
        return result
