

from sys import argv
# from hill_climber import Chip
from algorithms import hill_climber

if __name__ == "__main__":
    # check command line arguments
    if len(argv) != 3:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)

   
    hill_climber.main(argv[1], argv[2])

    


