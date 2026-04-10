import sys
from memory import Memory,SimulatorError
from CPU import CPU

def main():
    if len(sys.argv)<3:
        sys.exit(1)
    input_path=sys.argv[1]
    output_path=sys.argv[2]
    readable_path=sys.argv[3] if len(sys.argv)>3 else None

    try:
        with open(input_path,'r') as f:
            lines=f.readlines()

        mem_unit=Memory(lines)
        processor=CPU(mem_unit)

        history=[]
        ticks=0
        limit=100000

        while ticks<limit:
            try:
                active=processor.step()
                history.append(processor.traceLine())
                ticks+=1
                if not active:
                    break
            except SimulatorError as e:
                with open(output_path,'w') as f:
                    for line in history:
                        f.write(line+"\n")
                if readable_path:
                    with open(readable_path,'w') as f:
                        for line in history:
                            f.write(line+"\n")
                print(f"Error on line {e.lineno}: {e.message}")
                sys.exit(1)

        if ticks>=limit:
            raise SimulatorError(0,"Max step limit reached")

        final_mem=mem_unit.dumpData()
        output_lines=history+final_mem

        with open(output_path,'w') as f:
            for line in output_lines:
                f.write(line+"\n")

        if readable_path:
            with open(readable_path,'w') as f:
                for line in output_lines:
                    f.write(line+"\n")

    except SimulatorError as e:
        print(f"Error on line {e.lineno}: {e.message}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)

if __name__=="__main__":
    main()
