from registers import getRegisterCode
from binary import parseImm

# S-type encoding table: inst->(opcode_bits, funct3)
sTypeTable = {
    "sw": ("0100011", "010"),
}

# Syntax: sw rs2, imm(rs1)
def packSType(inst, operands):
    op, funct3 = sTypeTable[inst]
    rs2 = operands[0].strip()
    memRef = operands[1].strip()
    immStr, rs1 = memRef.split('(')
    rs1 = rs1.rstrip(')')
    immBin = parseImm(immStr, 12, signed=True)
    immUpper = immBin[0:7] # bits 11:5
    immLower = immBin[7:12] # bits 4:0
    return immUpper + getRegisterCode(rs2) + getRegisterCode(rs1) + funct3 + immLower + op
