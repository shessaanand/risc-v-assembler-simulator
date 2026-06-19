from errors import AssemblerError

def resolveOffset(token,currentPC,labelmap,lineno):
    token=token.strip()
    if token in labelmap: 
      return labelmap[token]-currentPC
    try:
        return int(token,0)
    except ValueError:
        raise AssemblerError(lineno, f"Label is undefined or immediate is invalid: '{token}'")
