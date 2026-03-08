from errors import AssemblerError
from registers import rMap

immbound = { "addi": (-2048, 2047), "lw": (-2048, 2047), "sltiu": (-2048, 2047), "jalr": (-2048, 2047),
    "sw": (-2048, 2047), "beq": (-4096, 4094), "bne": (-4096, 4094), "blt": (-4096, 4094), "bge": (-4096, 4094),
    "bltu": (-4096, 4094), "bgeu": (-4096, 4094), "lui": (-(1 << 19), (1 << 20) - 1), "auipc": (-(1 << 19), (1 << 20) - 1),
    "jal": (-(1 << 20), (1 << 20) - 2) }

def checkirange(inst, immval, lineno):
    if inst not in immbound:
        return
    lo, hi = immbound[inst]
    if not (lo <= immval <= hi):
        raise AssemblerError(lineno, f"Immediate {immval} out of range [{lo}, {hi}] for '{inst}'")

def checkreg(regname, lineno):
    regname = regname.strip().lower()
    if regname not in rMap:
        raise AssemblerError(lineno, f"Unknown register: '{regname}'")

def tokensplit(instrtxt):
    instrtxt= instrtxt.split('#')[0].strip()
    if not instrtxt:
        return None,[]
    parts= instrtxt.replace(',', ' ').split()
    inst= parts[0].lower()
    operands= parts[1:]
    return inst,operands

def extractlabel(rawline):
    if ':' in rawline:
        idx= rawline.index(':')
        labelpart= rawline[:idx].strip()
        remainder= rawline[idx+1:].strip()
        if labelpart and labelpart[0].isalpha():
            return labelpart, remainder
    return None,rawline
