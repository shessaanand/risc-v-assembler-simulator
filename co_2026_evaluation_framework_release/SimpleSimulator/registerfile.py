# registerfile.py
# Holds all 32 registers. x0 is hard-wired zero.
#shessaa will do

stackInitSP=0x0000017C

class RegisterFile:

    def __init__(self):
        self.regs=[0]*32
        self.regs[2]=stackInitSP   # sp = x2

    def read(self,idx):
        return self.regs[idx] & 0xFFFFFFFF

    def write(self,idx,value):
        if idx!=0:
            self.regs[idx]=value & 0xFFFFFFFF

    def dump(self):
        return [self.regs[i] & 0xFFFFFFFF for i in range(32)]
