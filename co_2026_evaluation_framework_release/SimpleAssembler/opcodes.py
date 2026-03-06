from encode_r import rTypeTable
from encode_i import iTypeTable
from encode_s import sTypeTable
from encode_b import bTypeTable
from encode_u import uTypeTable

maxInstructions=64 
knownOpcodes = {
    "add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and",
    "addi", "lw", "sltiu", "jalr",
    "sw",
    "beq", "bne", "blt", "bge", "bltu", "bgeu",
    "lui", "auipc",
    "jal",
    "nop",
}

opcodeType = {}
for _k in rTypeTable: 
  opcodeType[_k] = 'R'
for _k in iTypeTable: 
  opcodeType[_k] = 'I'
for _k in sTypeTable: 
  opcodeType[_k] = 'S'
for _k in bTypeTable: 
  opcodeType[_k] = 'B'
for _k in uTypeTable: 
  opcodeType[_k] = 'U'
opcodeType['jal'] = 'J'
