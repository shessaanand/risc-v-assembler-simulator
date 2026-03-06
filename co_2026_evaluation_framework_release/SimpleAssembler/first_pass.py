from errors import AssemblerError
from tokenizer import extractLabel

def buildLabelMap(lines):
    labelMap = {}
    instructionList = []
    currentAddr = 0x0
    for lineNumber, rawLine in lines:
        label, instrText = extractLabel(rawLine)
        if label:
            if label in labelMap: raise AssemblerError(lineNumber, f"Duplicate label: '{label}'")
            labelMap[label] = currentAddr
        if instrText == "": continue
        tokens = instrText.replace(',', ' ').split()
        inst = tokens[0].lower()
        instructionList.append((lineNumber, currentAddr, inst, instrText))
        currentAddr += 4
    return labelMap, instructionList
def checkVirtualHalt(instructionList):
    if not instructionList: raise AssemblerError(0, "No instructions found in program")
    for lineNumber, addr, inst, text in instructionList:
        tokens = text.replace(',', ' ').split()
        if (inst == "beq"
                and len(tokens) >= 4
                and tokens[1].lower() in ("zero", "x0")
                and tokens[2].lower() in ("zero", "x0")
                and tokens[3] in ("0", "0x0", "0x00000000", "0b0")):
            return
    raise AssemblerError(0, "Missing Virtual Halt instruction (beq zero, zero, 0)")
