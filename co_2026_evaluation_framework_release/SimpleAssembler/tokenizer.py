def splitIntoTokens(instrText):
    parts= instrText.replace(',', ' ').split()
    inst= parts[0].lower()
    operands= parts[1:]
    return inst,operands


def extractLabel(rawLine):
    if ':' in rawLine:
        idx= rawLine.index(':')
        labelPart= rawLine[:idx].strip()
        remainder= rawLine[idx + 1:].strip()
        if labelPart and labelPart[0].isalpha(): return labelPart, remainder
    return None,rawLine
