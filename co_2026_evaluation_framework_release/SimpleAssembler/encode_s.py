from registers import getRegisterCode
from binary import parseImm

sTypeTable = {"sw": ("0100011", "010")}

def packSType(inst, operands):
    op, funct3 = sTypeTable[inst]
    rs2= operands[0].strip()
    memRef = operands[1].strip()
    immStr,rs1 = memRef.split('(')
    rs1 = rs1.rstrip(')')
    immBin= parseImm(immStr, 12, signed=True)
    immUpper= immBin[0:7]
    immLower=immBin[7:12]
    return immUpper + getRegisterCode(rs2) + getRegisterCode(rs1) + funct3 + immLower + op

