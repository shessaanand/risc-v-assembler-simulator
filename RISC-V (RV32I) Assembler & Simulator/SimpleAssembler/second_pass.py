from errors import AssemblerError
from parsingF import tokensplit, checkreg, checkirange
from symbolsF import resolveOffset
from opcodes import knownopcodes, opcodeType, maxi

from R_I_encoding import packRType, packIType
from B_S_encoding import packSType, packBType
from U_J_encoding import packUType, packJType


def Binary(instructionList, labelMap):
    if len(instructionList) > maxi:
        raise AssemblerError(0, f"Program is {len(instructionList)} lines, its exceeding {maxi} lines")
    binaryop= []
    for lineno,currentadd,inst,instrtxt in instructionList:
        try:
            inst, operands = tokensplit(instrtxt)
            if inst not in knownopcodes: 
              raise AssemblerError(lineno, f"Unknown opcode: '{inst}'")
            if inst == "nop":
                inst = "addi"
                operands = ["x0", "x0", "0"]

            iType= opcodeType[inst]

            if iType == 'R':
                if len(operands) != 3: 
                  raise AssemblerError(lineno, f"'{inst}' requires 3 operands")
                for reg in operands: checkreg(reg, lineno)
                binary = packRType(inst, operands)

            elif iType == 'I':
                if inst in ("lw", "jalr") and len(operands) == 2:
                    checkreg(operands[0], lineno)
                    immstr, rs1 = operands[1].split('(')
                    checkreg(rs1.rstrip(')'), lineno)
                    checkirange(inst, int(immstr, 0), lineno)
                else:
                    if len(operands)!= 3:
                        raise AssemblerError(lineno, f"'{inst}' requires 3 operands")
                    checkreg(operands[0], lineno)
                    checkreg(operands[1],lineno)
                    checkirange(inst, int(operands[2],0),lineno)
                binary = packIType(inst,operands)

            elif iType == 'S':
                if len(operands)!= 2:
                    raise AssemblerError(lineno, f"'{inst}' requires 2 operands")
                checkreg(operands[0],lineno)
                immstr,rs1 = operands[1].split('(')
                checkreg(rs1.rstrip(')'),lineno)
                checkirange(inst,int(immstr, 0), lineno)
                binary=packSType(inst,operands)

            elif iType== 'B':
                if len(operands) != 3:
                    raise AssemblerError(lineno, f"'{inst}' requires 3 operands")
                checkreg(operands[0], lineno)
                checkreg(operands[1], lineno)
                branchOffset = resolveOffset(operands[2], currentadd, labelMap, lineno)
                checkirange(inst, branchOffset, lineno)
                binary = packBType(inst, operands[:2], branchOffset)

            elif iType=='U':
                if len(operands) != 2:
                    raise AssemblerError(lineno, f"'{inst}' requires 2 operands")
                checkreg(operands[0], lineno)
                checkirange(inst, int(operands[1], 0), lineno)
                binary = packUType(inst, operands)

            elif iType=='J':
                if len(operands) != 2:
                    raise AssemblerError(lineno, f"'{inst}' requires 2 operands")
                checkreg(operands[0], lineno)
                jumpOffset = resolveOffset(operands[1], currentadd, labelMap, lineno)
                checkirange(inst, jumpOffset, lineno)
                binary = packJType(inst, [operands[0]], jumpOffset)

            if len(binary)!= 32:
                raise AssemblerError(lineno, f"Encoder produced {len(binary)} bits for '{inst}'")
            binaryop.append(binary)

        except AssemblerError:
            raise
        except Exception as e:
            raise AssemblerError(lineno, str(e))

    return binaryop
