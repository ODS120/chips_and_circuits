from sys import argv
from algorithms import best_first
from algorithms import hill_climber

if __name__ == "__main__":
    # Check command line arguments
    if len(argv) != 3:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)
    
    # Ask user which algorithm to use
    user_input = None
    
    while user_input == None:
        user_input = int(input("Would you like to run the Best-First algorithm or the Hill-Climber algorithm?\nChoose 1 or 2\n 1. Best-First algorithm\n 2. Hill-Climber algorithm\n"))
        if user_input == 1:
            print("Best First algorithm\n")
            best_first.main(argv[1], argv[2])
        elif user_input == 2:
            print("Hill climber algorithm\n")
            hill_climber.main(argv[1], argv[2])
        else: 
            print("Wrong input\n")

