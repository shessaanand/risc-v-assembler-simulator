def toSignedBinary(value, numBits):
    if value< 0: 
      value = (1<<numBits)+value
    return format(value, f'0{numBits}b')


def parseImm(token, numBits, signed=True):
    value= int(token.strip(), 0)
    if signed:
        lo,hi = -(1 << (numBits - 1)), (1 << (numBits - 1)) - 1
    else:
        lo,hi = 0, (1 << numBits) - 1
    if not (lo <= value <= hi): 
      raise ValueError(f"Immediate {token} out of range [{lo}, {hi}] for {numBits}-bit field")
    return toSignedBinary(value, numBits)
