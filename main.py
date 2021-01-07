

from sys import argv
from classes import Chip, Coordinate, Gate

if __name__ == "__main__":
    # check command line arguments
    if len(argv) != 2:
        print("Usage: 'python main.py [print_x] [netlist_y]")
        exit(1)
    # create chip object from 'print data'
    chip = Chip(argv[1])

    # visualize grid
    # width = 6
    # height = 6
    # for y in range(height):
    #     for x in range(width):
    #         x1 = [x, x+1]
    #         x2 = [x, x]
    #         y1 = [y, y]
    #         y2 = [y, y+1]
    #         plt.plot(x1, y1, 'b', x2, y2, 'b')
    # plt.plot(x1, y1, 'b', x2, y2, 'b')
    # x3 = [3]
    # y3 = [3]
    # plt.plot(x3, y3, 'ro')



    # plt.xlim([0, 5])
    # plt.ylim([5, 0])
    # plt.xlim([0, chip.width()])
    # plt.ylim([chip.height(), 0])
    # # plt.legend()
    # # plt.xticks([])
    # # plt.yticks([])
    # plt.axis('off')
    # plt.show()
    # plt.savefig('test.png')