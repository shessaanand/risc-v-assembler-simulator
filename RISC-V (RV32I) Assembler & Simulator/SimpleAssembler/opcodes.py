from R_I_encoding import rTypeTable, iTypeTable
from B_S_encoding import sTypeTable, bTypeTable
from U_J_encoding import uTypeTable

maxi=64 
knownopcodes = { "add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and",
    "addi", "lw", "sltiu", "jalr", "sw", "beq", "bne", "blt", "bge", "bltu", "bgeu",
    "lui", "auipc", "jal", "nop" }

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
