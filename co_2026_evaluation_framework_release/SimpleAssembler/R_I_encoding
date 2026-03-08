from binary import pimm
from registers import getRcode

rTypeTable = {
    "add": ("0110011", "000", "0000000"),
    "sub": ("0110011", "000", "0100000"),
    "sll": ("0110011", "001", "0000000"),
    "slt": ("0110011", "010", "0000000"),
    "sltu": ("0110011", "011", "0000000"),
    "xor": ("0110011", "100", "0000000"),
    "srl": ("0110011", "101", "0000000"),
    "or": ("0110011", "110", "0000000"),
    "and": ("0110011", "111", "0000000")
}


def packRType(inst, operands):
    op, funct3, funct7 = rTypeTable[inst]
    rd, rs1,rs2=[o.strip() for o in operands]
    return funct7+getRcode(rs2)+getRcode(rs1)+funct3+getRcode(rd)+op

iTypeTable = {"lw": ("0000011", "010"), "addi": ("0010011", "000"), "sltiu": ("0010011", "011"),"jalr": ("1100111", "000")} 


def packIType(inst, operands):
    op, funct3 = iTypeTable[inst]
    if len(operands) == 2:
        rd = operands[0].strip()
        memRef = operands[1].strip()
        immStr, rs1 = memRef.split('(')
        rs1 = rs1.rstrip(')')
    else:
        rd, rs1, immStr = [o.strip() for o in operands]
    immBin = pimm(immStr, 12, signed=True)
    return immBin + getRcode(rs1) + funct3 + getRcode(rd) + op
