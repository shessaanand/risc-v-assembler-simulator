def signedbinary(value, numbits):
    if value< 0: 
      value = (1<<numbits)+value
    return format(value, f'0{numbits}b')


def pimm(token, numbits, signed=True):
    value= int(token.strip(), 0)
    if signed:
        lo,hi = -(1 << (numbits - 1)), (1 << (numbits - 1)) - 1
    else:
        lo,hi = 0, (1 << numbits) - 1
    if not (lo <= value <= hi): 
      raise ValueError(f"Immediate {token} out of range [{lo}, {hi}] for {numbits}-bit field")
    return signedbinary(value, numbits)
