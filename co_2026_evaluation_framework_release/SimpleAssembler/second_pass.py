from errors import AssemblerError
from tokenizer import splitIntoTokens
from resolver import resolveOffset
from validator import checkRegister,checkImmRange
from opcodes import knownOpcodes,opcodeType,maxInstructions
from encode_r import packRType
from encode_i import packIType
from encode_s import packSType
from encode_b import packBType
from encode_u import packUType
from encode_j import packJType


def generateBinary(instructionList, labelMap):
    if len(instructionList) > maxInstructions:
        raise AssemblerError(0, f"Program too large: {len(instructionList)} instructions exceed the maximum of {maxInstructions}")
    binaryOutput= []
    for lineNumber,currentAddr,inst,instrText in instructionList:
        try:
            inst, operands = splitIntoTokens(instrText)
            if inst not in knownOpcodes: 
              raise AssemblerError(lineNumber, f"Unknown opcode: '{inst}'")
            if inst == "nop":
                inst = "addi"
                operands = ["x0", "x0", "0"]

            iType= opcodeType[inst]

            if iType == 'R':
                if len(operands) != 3: 
                  raise AssemblerError(lineNumber, f"'{inst}' expects 3 operands")
                for reg in operands: checkRegister(reg, lineNumber)
                binary = packRType(inst, operands)

            elif iType == 'I':
                if inst in ("lw", "jalr") and len(operands) == 2:
                    checkRegister(operands[0], lineNumber)
                    immStr, rs1 = operands[1].split('(')
                    checkRegister(rs1.rstrip(')'), lineNumber)
                    checkImmRange(inst, int(immStr, 0), lineNumber)
                else:
                    if len(operands)!= 3: raise AssemblerError(lineNumber, f"'{inst}' expects 3 operands")
                    checkRegister(operands[0], lineNumber)
                    checkRegister(operands[1],lineNumber)
                    checkImmRange(inst, int(operands[2],0),lineNumber)
                binary = packIType(inst,operands)

            elif iType == 'S':
                if len(operands)!= 2: raise AssemblerError(lineNumber, f"'{inst}' expects 2 operands")
                checkRegister(operands[0],lineNumber)
                immStr,rs1 = operands[1].split('(')
                checkRegister(rs1.rstrip(')'),lineNumber)
                checkImmRange(inst,int(immStr, 0), lineNumber)
                binary=packSType(inst,operands)

            elif iType== 'B':
                if len(operands) != 3: raise AssemblerError(lineNumber, f"'{inst}' expects 3 operands")
                checkRegister(operands[0], lineNumber)
                checkRegister(operands[1], lineNumber)
                branchOffset = resolveOffset(operands[2], currentAddr, labelMap, lineNumber)
                checkImmRange(inst, branchOffset, lineNumber)
                binary = packBType(inst, operands[:2], branchOffset)

            elif iType=='U':
                if len(operands) != 2: raise AssemblerError(lineNumber, f"'{inst}' expects 2 operands")
                checkRegister(operands[0], lineNumber)
                checkImmRange(inst, int(operands[1], 0), lineNumber)
                binary = packUType(inst, operands)

            elif iType=='J':
                if len(operands) != 2: raise AssemblerError(lineNumber, f"'{inst}' expects 2 operands")
                checkRegister(operands[0], lineNumber)
                jumpOffset = resolveOffset(operands[1], currentAddr, labelMap, lineNumber)
                checkImmRange(inst, jumpOffset, lineNumber)
                binary = packJType(inst, [operands[0]], jumpOffset)

            if len(binary)!= 32: raise AssemblerError(lineNumber, f"Encoder produced {len(binary)} bits for '{inst}'")
            binaryOutput.append(binary)

        except AssemblerError:
            raise
        except Exception as e:
            raise AssemblerError(lineNumber, str(e))

    return binaryOutput
