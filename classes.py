import matplotlib.pyplot as plt
import numpy

class Chip():
    def __init__(self, filename):
        self.height = 0
        self.width = 0
        self.coordinates = []

        self.load_grid(filename)
        self.plot_chip()
        self.load_coordinates()
        self.load_gates(filename)

        plt.xlim([0, self.width - 1])
        plt.ylim([0, self.height - 1])
        # plt.legend()
        # plt.xticks([])
        # plt.yticks([])
        # plt.axis('off')
        plt.show()
        plt.savefig('test.png')


    # load the grid
    def load_grid(self, filename):
        with open(filename) as chip_grid:
            next(chip_grid)

            # find the max x and y coordinate
            for line in chip_grid:
                coordinates = line.split(",")

                if int(coordinates[1]) > self.width:
                    self.width = int(coordinates[1])

                if int(coordinates[2]) > self.height:
                    self.height = int(coordinates[2])
            
            # add borders to the grid
            self.width += 2
            self.height += 2
            self.coordinates = [[0 for x in range(self.width)] for y in range(self.height)]
            print(self.coordinates)            


    def plot_chip(self):
        for y in range(self.height):
            for x in range(self.width):
                x1 = [x, x+1]
                x2 = [x, x]
                y1 = [y, y]
                y2 = [y, y+1]
                plt.plot(x1, y1, 'b', x2, y2, 'b')


    # load all the coordinate classes
    def load_coordinates(self):
        # iterate over all the grid coordinates
        for y_coord in range(self.height):
            for x_coord in range(self.width):
                coordinate = Coordinate(x_coord, y_coord)
                self.coordinates[y_coord][x_coord] = coordinate


    # load all the gate classes
    def load_gates(self, filename):
        with open(filename) as chip_grid:
            next(chip_grid)

            for line in chip_grid:
                gate_info = line.split(",")
                gate_object = Gate(gate_info[0], gate_info[1], gate_info[2])
                
                # plot the gate onto the chip
                gate_x = int(gate_info[1])
                gate_y = int(gate_info[2])
                plt.plot(gate_x, gate_y, 'ro')

                # appoint the gate its position on the grid
                self.coordinates[gate_x][gate_y].gate = gate_object


class Coordinate(): 
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.gate = []
        # north, east, south, west, up, down
        self.connections = []   


class Gate():
    def __init__(self, gate_id, x, y):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y
