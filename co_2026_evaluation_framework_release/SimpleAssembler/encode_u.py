from registers import getRegisterCode
from binary import toSignedBinary

uTypeTable = {
    "lui": "0110111",
    "auipc": "0010111",
}

#Syntax: op rd, imm
def packUType(inst, operands):
    op = uTypeTable[inst]
    rd, immStr = [o.strip() for o in operands]
    immValue = int(immStr, 0)
    if not (-(1 << 19) <= immValue <= (1 << 20) - 1): raise ValueError(f"Immediate {immStr} out of range for 20-bit U-type field")
    immBin = toSignedBinary(immValue, 20)
    return immBin + getRegisterCode(rd) + op
