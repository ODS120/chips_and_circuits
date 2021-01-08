

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


# OUTPUT
# net,wires
# (1,2),"[(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]"
# (1,3),"[(1,5),(1,4),(2,4),(3,4),(4,4)]"
# (3,5),"[(4,4),(4,3),(3,3),(2,3),(1,3),(0,3),(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(3,1)]"
# (4,2),"[(6,2),(5,2),(5,3),(5,4),(6,4),(6,5)]"
# (4,5),"[(3,1),(4,1),(5,1),(6,1),(7,1),(7,2),(6,2)]"
# chip_0_net_1,32

# python3 main.py data/chip_0/print_0.csv data/chip_0/netlist_1.csv