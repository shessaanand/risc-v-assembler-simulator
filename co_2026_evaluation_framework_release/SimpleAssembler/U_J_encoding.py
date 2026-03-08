from registers import getRcode
from binary import signedbinary

JAL_OPCODE = "1101111"

def packJType(inst, operands, jumpOffset):
    rd = operands[0].strip()
    if not (-(1 << 20) <= jumpOffset<= (1 << 20)-2): 
      raise ValueError(f"JAL offset {jumpOffset} out of range")
    if jumpOffset % 2 != 0: 
      raise ValueError(f"JAL offset {jumpOffset} must be even")
        
    immBin= signedbinary(jumpOffset, 21)
    imm20 =immBin[0] 
    imm19_12 =immBin[1:9] 
    imm11= immBin[9] 
    imm10_1= immBin[10:20] 
    scrambled=imm20 + imm10_1 + imm11 + imm19_12
    return scrambled + getRcode(rd) + JAL_OPCODE

uTypeTable = {"lui": "0110111", "auipc": "0010111"}

def packUType(inst, operands):
    op = uTypeTable[inst]
    rd, immStr = [o.strip() for o in operands]
    immValue = int(immStr, 0)
    encoded = immValue >> 12
    if not (-(1<<19)<=encoded<=(1<<19)-1):
        raise ValueError("Immediate out of range")
    immBin=signedbinary(encoded,20)
    return immBin+getRcode(rd)+ op
