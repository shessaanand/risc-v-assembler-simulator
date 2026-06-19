from registers import getRcode
from binary import signedbinary
from binary import pimm

bTypeTable = {"beq": ("1100011", "000"),"bne": ("1100011", "001"),"blt": ("1100011", "100"),"bge": ("1100011", "101"),"bltu": ("1100011", "110"),"bgeu": ("1100011", "111")}
sTypeTable = {"sw": ("0100011", "010")}

def packBType(inst, ops, boff):
    op, funct3= bTypeTable[inst]
    rs1, rs2= (o.strip() for o in ops)

    if not (-4096 <= boff <= 4095):
        raise ValueError(f"Check - Branch offset {boff} is out of range")
    if boff %2 !=0:
        raise ValueError(f"Check - Branch offset {boff} should be even")
    
    immb= signedbinary(boff, 13)
    imm12= immb[0]
    imm11=immb[1]
    imm105= immb[2:8]
    imm41= immb[8:12]
    instu=imm12+imm105
    instl= imm41+imm11
    return instu + getRcode(rs2) + getRcode(rs1) + funct3 +instl +op

def packSType(inst, ops):
    op, funct3 = sTypeTable[inst]
    rs2 = ops[0].strip()
    mr= ops[1].strip()
    immstr, rs1 = mr.split('(')
    rs1 = rs1.rstrip(')')
    immb = pimm(immstr, 12, signed=True)
    immu = immb[0:7]
    imml = immb[7:12]
    return immu + getRcode(rs2) + getRcode(rs1) + funct3 + imml + op
