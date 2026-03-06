from registers import getRegisterCode
from binary import toSignedBinary

# B-type encoding table: inst -> (opcode_bits, funct3)
bTypeTable = {
    "beq": ("1100011", "000"),
    "bne": ("1100011", "001"),
    "blt": ("1100011", "100"),
    "bge": ("1100011", "101"),
    "bltu": ("1100011", "110"),
    "bgeu": ("1100011", "111"),
}

# Syntax: op rs1, rs2, offset (offset already resolved to integer)
def packBType(inst, operands, branchOffset):
    op, funct3= bTypeTable[inst]
    rs1, rs2= [o.strip() for o in operands]
    if not (-4096 <= branchOffset <= 4094): raise ValueError(f"Branch offset {branchOffset} out of range")
    if branchOffset % 2 != 0: raise ValueError(f"Branch offset {branchOffset} must be even")
    immBin= toSignedBinary(branchOffset, 13)
    imm12= immBin[0]  
    imm11=immBin[1]  
    imm105= immBin[2:8]  
    imm41= immBin[8:12] 
    instUpper=imm12 + imm105  
    instLower= imm41 + imm11 
    return instUpper + getRegisterCode(rs2) + getRegisterCode(rs1) + funct3 + instLower + op
