import sys
from errors import AssemblerError
from first_pass import buildLMap, checkVhalt
from second_pass import Binary

def readFile(filepath):
    with open(filepath, 'r') as f:
        rawLines= f.readlines()
    cleanedLines= []
    for lineno,line in enumerate(rawLines, start=1):
        stripped= line.strip()
        if stripped== "" or stripped.startswith("#"): 
            continue
        cleanedLines.append((lineno,stripped))
    return cleanedLines
  
def main():
    if len(sys.argv)<3:
        print("Format is - python assembler.py <input.asm> <output.txt>")
        sys.exit(1)

    inputpath=sys.argv[1]
    outputpath=sys.argv[2]

    try:
        sourcelines=readFile(inputpath)
        lMap,iList = buildLMap(sourcelines)
        checkVhalt(iList)
        binaryop= Binary(iList, lMap)
        with open(outputpath, 'w') as f:
            for b in binaryop:
                f.write(b + '\n')
    except AssemblerError as e:
        print(f"Error on line {e.lineno}: {e.message}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{inputpath}' not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
