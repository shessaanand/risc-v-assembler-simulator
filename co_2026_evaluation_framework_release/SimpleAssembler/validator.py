from errors import AssemblerError
from registers import registerMap
immBounds = {
    "addi": (-2048, 2047),
    "lw": (-2048, 2047),
    "sltiu": (-2048, 2047),
    "jalr": (-2048, 2047),
    "sw": (-2048, 2047),
    "beq": (-4096, 4094),
    "bne": (-4096, 4094),
    "blt": (-4096, 4094),
    "bge": (-4096, 4094),
    "bltu": (-4096, 4094),
    "bgeu": (-4096, 4094),
    "lui": (-(1 << 19), (1 << 20) - 1),
    "auipc": (-(1 << 19), (1 << 20) - 1),
    "jal": (-(1 << 20), (1 << 20) - 2),
}

def checkImmRange(inst, immValue, lineNumber):
    if inst not in immBounds: return
    lo, hi = immBounds[inst]
    if not (lo <= immValue <= hi): raise AssemblerError(lineNumber, f"Immediate {immValue} out of range [{lo}, {hi}] for '{inst}'")
def checkRegister(regName, lineNumber):
    regName = regName.strip().lower()
    if regName not in registerMap: raise AssemblerError(lineNumber, f"Unknown register: '{regName}'")
def checkImmRange(inst, immValue, lineNumber):
    if inst not in immBounds: return
    lo, hi = immBounds[inst]
    if not (lo <= immValue <= hi): raise AssemblerError(lineNumber, f"Immediate {immValue} out of range [{lo}, {hi}] for '{inst}'")
def checkRegister(regName, lineNumber):
    regName = regName.strip().lower()
    if regName not in registerMap: raise AssemblerError(lineNumber, f"Unknown register: '{regName}'")
