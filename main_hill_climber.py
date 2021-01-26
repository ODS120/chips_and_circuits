'''
Jan-Joost Raedts, Olaf Stringer, Martijn van Veen,

Hill Climber based algorithm
'''

from sys import argv
from algorithms import hill_climber

if __name__ == "__main__":
    # Check command line arguments
    if len(argv) != 3:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)
   
    hill_climber.main(argv[1], argv[2])

    


