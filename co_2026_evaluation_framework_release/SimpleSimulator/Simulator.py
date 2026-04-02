import sys
from memory import Memory,SimulatorError
from CPU import CPU

# puneet's work:

def main():
   
    # Implement the simulator driver logic here.
    
    # Steps to follow:
    
    # 1. Check command line arguments
    #    - Minimum required: input file and output file
    #    - Optional: readable output file
    #    - If arguments missing, print usage message and exit
    
    # 2. Read input file
    #    - Open input file
    #    - Read all binary instruction lines
    
    # 3. Initialize simulator
    #    - Create Memory object using binary lines
    #    - Create CPU object using memory
    
    # 4. Execute simulation loop
    #    - Run CPU step repeatedly
    #    - Stop when:
    #        a) virtual halt occurs
    #        b) error occurs
    #        c) max step limit reached
    
    # 5. Track execution
    #    - Maintain step counter
    #    - Store trace output using cpu.traceLine()
    
    # 6. Handle errors
    #    - Catch SimulatorError
    #    - Stop execution
    
    # 7. Dump memory contents
    #    - After successful execution
    #    - Append memory dump to output
    
    # 8. Write output file
    #    - Write trace + memory dump
    
    # 9. Write readable file (optional)
    #    - If readable file path provided
    #    - Write same output
    
    # 10. Handle exceptions
    #     - File not found
    #     - Simulator errors




if __name__=="__main__":
    main()
