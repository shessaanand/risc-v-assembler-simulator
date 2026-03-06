from registers import getRegisterCode

rTypeTable = {
    "add": ("0110011", "000", "0000000"),
    "sub": ("0110011", "000", "0100000"),
    "sll": ("0110011", "001", "0000000"),
    "slt": ("0110011", "010", "0000000"),
    "sltu": ("0110011", "011", "0000000"),
    "xor": ("0110011", "100", "0000000"),
    "srl": ("0110011", "101", "0000000"),
    "or": ("0110011", "110", "0000000"),
    "and": ("0110011", "111", "0000000"),
}


def packRType(inst, operands):
    op, funct3, funct7 = rTypeTable[inst]
    rd, rs1,rs2=[o.strip() for o in operands]
    return funct7+getRegisterCode(rs2)+getRegisterCode(rs1)+funct3+getRegisterCode(rd)+op
