import sys

REGISTER_MAP = {
    "zero": "00000", "x0":  "00000",
    "ra":   "00001", "x1":  "00001",
    "sp":   "00010", "x2":  "00010",
    "gp":   "00011", "x3":  "00011",
    "tp":   "00100", "x4":  "00100",
    "t0":   "00101", "x5":  "00101",
    "t1":   "00110", "x6":  "00110",
    "t2":   "00111", "x7":  "00111",
    "s0":   "01000", "fp":  "01000", "x8":  "01000",
    "s1":   "01001", "x9":  "01001",
    "a0":   "01010", "x10": "01010",
    "a1":   "01011", "x11": "01011",
    "a2":   "01100", "x12": "01100",
    "a3":   "01101", "x13": "01101",
    "a4":   "01110", "x14": "01110",
    "a5":   "01111", "x15": "01111",
    "a6":   "10000", "x16": "10000",
    "a7":   "10001", "x17": "10001",
    "s2":   "10010", "x18": "10010",
    "s3":   "10011", "x19": "10011",
    "s4":   "10100", "x20": "10100",
    "s5":   "10101", "x21": "10101",
    "s6":   "10110", "x22": "10110",
    "s7":   "10111", "x23": "10111",
    "s8":   "11000", "x24": "11000",
    "s9":   "11001", "x25": "11001",
    "s10":  "11010", "x26": "11010",
    "s11":  "11011", "x27": "11011",
    "t3":   "11100", "x28": "11100",
    "t4":   "11101", "x29": "11101",
    "t5":   "11110", "x30": "11110",
    "t6":   "11111", "x31": "11111",
}

KNOWN_OPCODES = {
    "add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and",
    "addi", "lw", "sltiu", "jalr",
    "sw",
    "beq", "bne", "blt", "bge", "bltu", "bgeu",
    "lui", "auipc",
    "jal",
    "nop",
}

IMM_BOUNDS = {
    "addi":  (-2048,2047),
    "lw":    (-2048,2047),
    "sltiu": (-2048,2047),
    "jalr":  (-2048,2047),
    "sw":    (-2048,2047),
    "beq":   (-4096,4094),
    "bne":   (-4096,4094),
    "blt":   (-4096,4094),
    "bge":   (-4096,4094),
    "bltu":  (-4096,4094),
    "bgeu":  (-4096,4094),
    "lui":   (-(1 << 19), (1 << 20) - 1),
    "auipc": (-(1 << 19), (1 << 20) - 1),
    "jal":   (-(1 << 20), (1 << 20) - 2),
}

MAX_INSTRUCTIONS = 64   # 256-byte program memory / 4 bytes each

class AssemblerError(Exception):
    def __init__(self, lineno, message):
        self.lineno  = lineno
        self.message = message
        super().__init__(f"Line {lineno}: {message}")


def to_signed_binary(value, bits):
    # Convert a signed integer to a 2's-complement binary string of `bits` width.
    if value < 0:
        value = (1 << bits) + value
    return format(value, f'0{bits}b')


def get_reg(name):
    # Return the 5-bit binary string for a register name.
    name = name.strip().lower()
    if name not in REGISTER_MAP:
        raise ValueError(f"Unknown register: '{name}'")
    return REGISTER_MAP[name]


def validate_register(name, lineno):
    # Raise AssemblerError if the register name is not recognised.
    name = name.strip().lower()
    if name not in REGISTER_MAP:
        raise AssemblerError(lineno, f"Unknown register: '{name}'")


def validate_imm(opcode, value, lineno):
    # Raise AssemblerError if the immediate is outside the allowed range.
    if opcode in IMM_BOUNDS:
        lo, hi = IMM_BOUNDS[opcode]
        if not (lo <= value <= hi):
            raise AssemblerError(
                lineno,
                f"Immediate {value} out of range [{lo}, {hi}] for '{opcode}'"
            )


def parse_imm(token, bits, signed=True):
    # Parse a token string as an integer and return its fixed-width binary string.
    value = int(token.strip(), 0)
    if signed:
        lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    else:
        lo, hi = 0, (1 << bits) - 1
    if not (lo <= value <= hi):
        raise ValueError(f"Immediate {token} out of range [{lo}, {hi}] for {bits}-bit field")
    return to_signed_binary(value, bits)


def parse_operands(instr_text):
    # Split "opcode op1, op2, op3" into (opcode, [op1, op2, op3]).
    parts    = instr_text.replace(',', ' ').split()
    opcode   = parts[0].lower()
    operands = parts[1:]
    return opcode, operands


def split_label(raw):
    # Return (label, rest) if the line has a label, otherwise (None, raw).
    if ':' in raw:
        idx        = raw.index(':')
        label_part = raw[:idx].strip()
        rest       = raw[idx + 1:].strip()
        if label_part and label_part[0].isalpha():
            return label_part, rest
    return None, raw


def resolve_offset(token, current_pc, label_map, lineno):
    # Convert a label name or numeric literal to a PC-relative integer offset.
    token = token.strip()
    if token in label_map:
        return label_map[token] - current_pc
    try:
        return int(token, 0)
    except ValueError:
        raise AssemblerError(lineno, f"Undefined label or invalid immediate: '{token}'")


def first_pass(lines):
    # Walk all lines once: build label_map and instruction list with addresses.
    label_map    = {}
    instructions = []
    address      = 0x0
    for lineno, raw in lines:
        label, instr_text = split_label(raw)
        if label:
            if label in label_map:
                raise AssemblerError(lineno, f"Duplicate label: '{label}'")
            label_map[label] = address
        if instr_text == "":
            continue
        tokens = instr_text.replace(',', ' ').split()
        opcode = tokens[0].lower()
        instructions.append((lineno, address, opcode, instr_text))
        address += 4
    return label_map, instructions


def check_virtual_halt(instructions):
    # Verify the program contains at least one "beq zero, zero, 0" halt.
    if not instructions:
        raise AssemblerError(0, "No instructions found in program")
    for lineno, addr, opcode, text in instructions:
        tokens = text.replace(',', ' ').split()
        if (opcode == "beq"
                and len(tokens) >= 4
                and tokens[1].lower() in ("zero", "x0")
                and tokens[2].lower() in ("zero", "x0")
                and tokens[3] in ("0", "0x0", "0x00000000", "0b0")):
            return
    raise AssemblerError(0, "Missing Virtual Halt instruction (beq zero, zero, 0)")



# =============================================================================
# PERSON 1  —  FILE HANDLING AND MAIN DRIVER
# =============================================================================
# Implement:
#   read_file()   — open and clean the source file
#   main()        — entry point, runs all passes, writes output
# =============================================================================

def read_file(path):
    # Open the source file and return (line_number, line_text) for every
    # non-blank, non-comment line.
    with open(path, 'r') as f:
        lines = f.readlines()
    result = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        result.append((i,stripped))
    return result


def main():
    # Entry point: parse arguments, run all passes, write binary output.
    if len(sys.argv)<3:
        print("Usage: python3 Assembler.py <input.asm> <output.txt>")
        sys.exit(1)

    input_path= sys.argv[1]
    output_path= sys.argv[2]

    try:
        lines= read_file(input_path)
        label_map, instructions= first_pass(lines)
        check_virtual_halt(instructions)
        binary_output= second_pass(instructions, label_map)

        with open(output_path, 'w') as f:
            for binary in binary_output:
                f.write(binary + '\n')

    except AssemblerError as e:
        print(f"Error on line {e.lineno}: {e.message}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

# =============================================================================
# PERSON 2  —  R-TYPE AND I-TYPE INSTRUCTIONS
# =============================================================================
# Implement:
#   encode_r()   — add, sub, sll, slt, sltu, xor, srl, or, and
#   encode_i()   — addi, lw, sltiu, jalr
# =============================================================================

# R-type encoding table: opcode -> (opcode_bits, funct3, funct7)
# Format: funct7[7] | rs2[5] | rs1[5] | funct3[3] | rd[5] | opcode[7]
R_TABLE = {
    "add":  ("0110011", "000", "0000000"),
    "sub":  ("0110011", "000", "0100000"),
    "sll":  ("0110011", "001", "0000000"),
    "slt":  ("0110011", "010", "0000000"),
    "sltu": ("0110011", "011", "0000000"),
    "xor":  ("0110011", "100", "0000000"),
    "srl":  ("0110011", "101", "0000000"),
    "or":   ("0110011", "110", "0000000"),
    "and":  ("0110011", "111", "0000000"),
}

def encode_r(opcode, operands):
    # Encode: add, sub, sll, slt, sltu, xor, srl, or, and
    # Syntax: op rd, rs1, rs2
    # Format: funct7 | rs2 | rs1 | funct3 | rd | opcode
    op, funct3, funct7 = R_TABLE[opcode]
    rd, rs1, rs2 = [o.strip() for o in operands]
    return funct7 + get_reg(rs2) + get_reg(rs1) + funct3 + get_reg(rd) + op


# I-type encoding table: opcode -> (opcode_bits, funct3)
# Format: imm[12] | rs1[5] | funct3[3] | rd[5] | opcode[7]
I_TABLE = {
    "lw":    ("0000011", "010"),
    "addi":  ("0010011", "000"),
    "sltiu": ("0010011", "011"),
    "jalr":  ("1100111", "000"),
}

def encode_i(opcode, operands):
    # Encode: lw, addi, sltiu, jalr
    # Syntax A (addi, sltiu): op rd, rs1, imm
    # Syntax B (lw, jalr): op rd, imm(rs1) or op rd, rs1, imm
    # Format: imm[11:0] | rs1 | funct3 | rd | opcode
    op, funct3 = I_TABLE[opcode]
    if len(operands)==2:
        rd = operands[0].strip()
        mem = operands[1].strip()
        imm_str, rs1 = mem.split('(')
        rs1 = rs1.rstrip(')')
    else:
        rd, rs1, imm_str = [o.strip() for o in operands]
    imm_bin = parse_imm(imm_str, 12, signed=True)
    return imm_bin + get_reg(rs1) + funct3 + get_reg(rd) + op


# =============================================================================
# PERSON 3  —  S-TYPE AND B-TYPE INSTRUCTIONS
# =============================================================================

# S-type encoding table: opcode -> (opcode_bits, funct3)
# Format: imm[11:5][7] | rs2[5] | rs1[5] | funct3[3] | imm[4:0][5] | opcode[7]
# Note: the 12-bit immediate is SPLIT — upper 7 bits at [31:25], lower 5 at [11:7]

S_TABLE = {
    "sw": ("0100011", "010"),
}

def encode_s(opcode, operands):
    # Encode: sw
    # Syntax: sw rs2, imm(rs1)
    # Format: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
    op, funct3 = S_TABLE[opcode]
    rs2= operands[0].strip()
    mem= operands[1].strip()
    imm_str, rs1 = mem.split('(')
    rs1= rs1.rstrip(')')
    imm_bin= parse_imm(imm_str, 12, signed=True)
    imm_upper= imm_bin[0:7]   # bits 11:5
    imm_lower= imm_bin[7:12]  # bits  4:0
    return imm_upper + get_reg(rs2) + get_reg(rs1) + funct3 + imm_lower + op


# B-type encoding table: opcode -> (opcode_bits, funct3)
# Format: imm[12|10:5][7] | rs2[5] | rs1[5] | funct3[3] | imm[4:1|11][5] | opcode[7]
# Note: 13-bit immediate is SCRAMBLED; offset must be even (bit 0 implicit).
B_TABLE = {
    "beq":("1100011", "000"),
    "bne":("1100011", "001"),
    "blt":("1100011", "100"),
    "bge":("1100011", "101"),
    "bltu":("1100011", "110"),
    "bgeu":("1100011", "111"),
}

def encode_b(opcode, operands, offset):
    # Encode: beq, bne, blt, bge, bltu, bgeu
    # Syntax: op rs1, rs2, offset  (offset already resolved)
    # Format: imm[12|10:5] | rs2 | rs1 | funct3 | imm[4:1|11] | opcode
    op, funct3 = B_TABLE[opcode]
    rs1, rs2= [o.strip() for o in operands]
    if not (-4096 <= offset <= 4094):
        raise ValueError(f"Branch offset {offset} out of range")
    if offset % 2 != 0:
        raise ValueError(f"Branch offset {offset} must be even")
    imm_bin= to_signed_binary(offset, 13)
    imm12= imm_bin[0]      # bit 12
    imm11= imm_bin[1]      # bit 11
    imm105= imm_bin[2:8]    # bits 10:5
    imm41= imm_bin[8:12]   # bits  4:1
    inst_upper= imm12 + imm105  # 7 bits -> [31:25]
    inst_lower= imm41 + imm11   # 5 bits -> [11:7]
    return inst_upper + get_reg(rs2) + get_reg(rs1) + funct3 + inst_lower + op


# =============================================================================
# PERSON 4  —  U-TYPE AND J-TYPE INSTRUCTIONS
# =============================================================================

# U-type encoding table: opcode -> opcode_bits
# Format: imm[31:12][20] | rd[5] | opcode[7]
U_TABLE = {
    "lui":"0110111",
    "auipc":"0010111",
}

def encode_u(opcode, operands):
    # Encode: lui, auipc
    # Syntax: op rd, imm
    # Format: imm[31:12] | rd | opcode
    op= U_TABLE[opcode]
    rd, imm_str= [o.strip() for o in operands]
    value= int(imm_str, 0)
    if not (-(1 << 19) <= value <= (1 << 20) - 1):
        raise ValueError(f"Immediate {imm_str} out of range for 20-bit U-type field")
    imm_bin= to_signed_binary(value, 20)
    return imm_bin + get_reg(rd) + op


# J-type: only one instruction (jal).
# Format: imm[20|10:1|11|19:12][20] | rd[5] | opcode[7]
# Note: 21-bit immediate is SCRAMBLED; offset must be even (bit 0 implicit).

def encode_j(opcode, operands, offset):
    # Encode: jal
    # Syntax: jal rd, offset  (offset already resolved)
    # Format: imm[20|10:1|11|19:12] | rd | opcode
    op ="1101111"
    rd =operands[0].strip()
    if not (-(1 << 20) <= offset <= (1 << 20) - 2):
        raise ValueError(f"JAL offset {offset} out of range")
    if offset % 2 != 0:
        raise ValueError(f"JAL offset {offset} must be even")
    imm_bin= to_signed_binary(offset, 21)
    imm20= imm_bin[0]      # bit 20
    imm19_12= imm_bin[1:9]    # bits 19:12
    imm11= imm_bin[9]      # bit 11
    imm10_1= imm_bin[10:20]  # bits 10:1
    encoded= imm20 + imm10_1 + imm11 + imm19_12  # 20 bits
    return encoded + get_reg(rd) + op


# Instruction type map — built from the encode tables above.
OPCODE_TYPE = {}
for _k in R_TABLE: 
    OPCODE_TYPE[_k] = 'R'
for _k in I_TABLE: 
    OPCODE_TYPE[_k] = 'I'
for _k in S_TABLE: 
    OPCODE_TYPE[_k] = 'S'
for _k in B_TABLE: 
    OPCODE_TYPE[_k] = 'B'
for _k in U_TABLE: 
    OPCODE_TYPE[_k] = 'U'
    
OPCODE_TYPE['jal'] = 'J'


def second_pass(instructions, label_map):
    # Encode every instruction to a 32-bit binary string.
    # Returns a list of binary strings, one per instruction.
    if len(instructions)>MAX_INSTRUCTIONS:
        raise AssemblerError(0, f"Program too large: {len(instructions)} instructions "
                                f"exceed the maximum of {MAX_INSTRUCTIONS}")

    binary_output = []

    for lineno,address,opcode,instr_text in instructions:
        try:
            opcode, operands= parse_operands(instr_text)

            if opcode not in KNOWN_OPCODES:
                raise AssemblerError(lineno, f"Unknown opcode: '{opcode}'")

            # Expand nop pseudo-instruction -> addi x0, x0, 0
            if opcode == "nop":
                opcode= "addi"
                operands= ["x0", "x0", "0"]

            itype = OPCODE_TYPE[opcode]

            if itype == 'R':
                if len(operands) != 3:
                    raise AssemblerError(lineno, f"'{opcode}' expects 3 operands")
                for reg in operands:
                    validate_register(reg, lineno)
                binary= encode_r(opcode, operands)

            elif itype== 'I':
                if opcode in ("lw", "jalr") and len(operands) == 2:
                    validate_register(operands[0], lineno)
                    imm_str, rs1 = operands[1].split('(')
                    validate_register(rs1.rstrip(')'), lineno)
                    validate_imm(opcode, int(imm_str, 0), lineno)
                else:
                    if len(operands) != 3:
                        raise AssemblerError(lineno, f"'{opcode}' expects 3 operands")
                    validate_register(operands[0], lineno)
                    validate_register(operands[1],lineno)
                    validate_imm(opcode, int(operands[2],0),lineno)
                binary = encode_i(opcode,operands)

            elif itype == 'S':
                if len(operands) != 2:
                    raise AssemblerError(lineno, f"'{opcode}' expects 2 operands")
                validate_register(operands[0], lineno)
                imm_str, rs1 = operands[1].split('(')
                validate_register(rs1.rstrip(')'), lineno)
                validate_imm(opcode, int(imm_str, 0), lineno)
                binary = encode_s(opcode, operands)

            elif itype== 'B':
                if len(operands) != 3:
                    raise AssemblerError(lineno, f"'{opcode}' expects 3 operands")
                validate_register(operands[0],lineno)
                validate_register(operands[1],lineno)
                offset = resolve_offset(operands[2], address, label_map, lineno)
                validate_imm(opcode, offset, lineno)
                binary = encode_b(opcode, operands[:2], offset)

            elif itype== 'U':
                if len(operands) != 2:
                    raise AssemblerError(lineno, f"'{opcode}' expects 2 operands")
                validate_register(operands[0], lineno)
                validate_imm(opcode, int(operands[1], 0), lineno)
                binary = encode_u(opcode, operands)

            elif itype== 'J':
                if len(operands) != 2:
                    raise AssemblerError(lineno, f"'{opcode}' expects 2 operands")
                validate_register(operands[0],lineno)
                offset =resolve_offset(operands[1],address,label_map,lineno)
                validate_imm(opcode,offset,lineno)
                binary= encode_j(opcode, [operands[0]],offset)

            if len(binary)!=32:
                raise AssemblerError(lineno, f"Encoder produced {len(binary)} bits for '{opcode}'")

            binary_output.append(binary)

        except AssemblerError:
            raise
        except Exception as e:
            raise AssemblerError(lineno str(e))

    return binary_output


# =============================================================================
if __name__ == "__main__":
    main()
