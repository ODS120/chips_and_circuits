

from sys import argv
# from hill_climber import Chip
from hill_climb_serie_3 import Chip

if __name__ == "__main__":
    # check command line arguments
    if len(argv) != 3:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)

    # create chip object from files
 
    chip = Chip(argv[1], argv[2])

    


