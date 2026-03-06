from registers import getRegisterCode
from binary import parseImm

iTypeTable = {
    "lw": ("0000011", "010"),
    "addi": ("0010011", "000"),
    "sltiu": ("0010011", "011"),
    "jalr": ("1100111", "000"),
}


def packIType(inst, operands):
    op, funct3 = iTypeTable[inst]
    if len(operands) == 2:
        rd = operands[0].strip()
        memRef = operands[1].strip()
        immStr, rs1 = memRef.split('(')
        rs1 = rs1.rstrip(')')
    else:
        rd, rs1, immStr = [o.strip() for o in operands]
    immBin = parseImm(immStr, 12, signed=True)
    return immBin + getRegisterCode(rs1) + funct3 + getRegisterCode(rd) + op
