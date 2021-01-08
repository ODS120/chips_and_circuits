

from sys import argv
from classes import Chip#, Coordinate, Gate

if __name__ == "__main__":
    # check command line arguments
    if len(argv) != 3:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)

    # create chip object from files
 
    chip = Chip(argv[1], argv[2])

    

# import csv
# with open('innovators.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["SN", "Name", "Contribution"])
#     writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
#     writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
#     writer.writerow([3, "Guido van Rossum", "Python Programming"])

# SN,Name,Contribution
# 1,Linus Torvalds,Linux Kernel
# 2,Tim Berners-Lee,World Wide Web
# 3,Guido van Rossum,Python Programming
