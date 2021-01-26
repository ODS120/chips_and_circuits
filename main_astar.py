

from sys import argv
from algorithms import astar_old

if __name__ == "__main__":
    # Check command line arguments
    if len(argv) != 3:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)
 
    astar_old.main(argv[1], argv[2])
