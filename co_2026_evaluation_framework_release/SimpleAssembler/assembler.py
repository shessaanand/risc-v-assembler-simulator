import sys
from errors import AssemblerError
from first_pass import buildLabelMap, checkVirtualHalt
from second_pass import generateBinary

def readSourceFile(filePath):
    with open(filePath, 'r') as f:
        rawLines= f.readlines()
    cleanedLines= []
    for lineNumber,line in enumerate(rawLines, start=1):
        stripped= line.strip()
        if stripped== "" or stripped.startswith("#"): continue
        cleanedLines.append((lineNumber,stripped))
    return cleanedLines
  
def main():
    if len(sys.argv)< 3:
        print("Usage: python3 assembler.py <input.asm> <output.txt>")
        sys.exit(1)

    inputPath= sys.argv[1]
    outputPath= sys.argv[2]

    try:
        sourceLines= readSourceFile(inputPath)
        labelMap, instructionList = buildLabelMap(sourceLines)
        checkVirtualHalt(instructionList)
        binaryOutput= generateBinary(instructionList, labelMap)
        with open(outputPath, 'w') as f:
            for binaryLine in binaryOutput:
                f.write(binaryLine + '\n')
    except AssemblerError as e:
        print(f"Error on line {e.lineNumber}: {e.message}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{inputPath}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
