from errors import AssemblerError

def resolveOffset(token,currentPC,labelMap,lineNumber):
    token=token.strip()
    if token in labelMap: 
      return labelMap[token] -currentPC
    try:
        return int(token,0)
    except ValueError:
        raise AssemblerError(lineNumber, f"Undefined label or invalid immediate: '{token}'")
