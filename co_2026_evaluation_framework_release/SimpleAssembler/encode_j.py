from registers import getRegisterCode
from binary import toSignedBinary

JAL_OPCODE = "1101111"

# Syntax: jal rd, offset (offset already resolved to integer)
def packJType(inst, operands, jumpOffset):
    rd = operands[0].strip()
    if not (-(1 << 20) <= jumpOffset<= (1 << 20)-2): 
      raise ValueError(f"JAL offset {jumpOffset} out of range")
    if jumpOffset % 2 != 0: 
      raise ValueError(f"JAL offset {jumpOffset} must be even")
    immBin= toSignedBinary(jumpOffset, 21)
    imm20 =immBin[0] 
    imm19_12 =immBin[1:9] 
    imm11= immBin[9] 
    imm10_1= immBin[10:20] 
    scrambled=imm20 + imm10_1 + imm11 + imm19_12
    return scrambled + getRegisterCode(rd) + JAL_OPCODE
