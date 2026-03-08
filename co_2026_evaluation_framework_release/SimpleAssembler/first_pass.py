from errors import AssemblerError
from parsingF import extractlabel

def buildLMap(lines):
    labelmap = {}
    iList = []
    currentadd = 0x0
    for lineno, rawline in lines:
        label, instrtxt = extractlabel(rawline)
        if label:
            if label in labelmap: 
                raise AssemblerError(lineno, f"Label is duplicate: '{label}'")
            labelmap[label] = currentadd
        if instrtxt == "": 
            continue
        tokens = instrtxt.replace(',', ' ').split()
        inst = tokens[0].lower()
        iList.append((lineno, currentadd, inst, instrtxt))
        currentadd += 4
    return labelmap, iList

def checkVhalt(iList):
    if not iList: 
        raise AssemblerError(0, "No instructions found in program")
    for lineno, addr, inst, text in iList:
        tokens = text.replace(',', ' ').split()
        if (inst == "beq"
                and len(tokens) >= 4
                and tokens[1].lower() in ("zero", "x0")
                and tokens[2].lower() in ("zero", "x0")
                and tokens[3] in ("0", "0x0", "0x00000000", "0b0")):
            return
    raise AssemblerError(0, "Virtual halt instruction is missing - (beq zero, zero, 0)")
