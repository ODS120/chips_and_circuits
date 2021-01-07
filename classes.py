import matplotlib.pyplot as plt


class Chip():
    def __init__(self, chip_data, netlist):
        self.height = 0
        self.width = 0
        self.coordinates = []
        self.gates = {}

        self.load_grid(chip_data)
        self.plot_chip()
        self.load_coordinates()
        self.load_gates()
        self.draw_wires(netlist)

        plt.xlim([0, self.width - 1])
        plt.ylim([0, self.height - 1])
        # plt.legend()
        # plt.xticks([])
        # plt.yticks([])
        # plt.axis('off')
        plt.show()
        plt.savefig('test.png')


    # load the grid
    def load_grid(self, chip_data):
        with open(chip_data) as chip_grid:
            next(chip_grid)

            for line in chip_grid:
                gate_info = line.strip("\n").split(",")
                self.gates[gate_info[0]] = {"x_coord": int(gate_info[1]), "y_coord": int(gate_info[2])}

                # find the max x and y coordinate
                if int(gate_info[1]) > self.width:
                    self.width = int(gate_info[1])

                if int(gate_info[2]) > self.height:
                    self.height = int(gate_info[2])
            
            # add borders to the grid
            self.width += 2
            self.height += 2

            # fill the grid
            self.coordinates = [[0 for x in range(self.width)] for y in range(self.height)]         


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
    def load_gates(self):
        for gate_id in self.gates:
            gate = self.gates[gate_id]
            gate_object = Gate(gate_id, gate["x_coord"], gate["y_coord"])

            # plot the gate onto the chip
            plt.plot(gate["x_coord"], gate["y_coord"], 'ro', marker = "s", markersize = 20)

            # plot gate label 
            plt.annotate(f"{gate_id}", (gate["x_coord"], gate["y_coord"]), fontsize = 13, ha = "center", va = "center")

            # appoint the gate its position on the grid
            self.coordinates[gate["x_coord"]][gate["y_coord"]].gate = gate_object


    def draw_wires(self, file):
        with open(file) as netlist:
            next(netlist)

            for line in netlist:
                connection = line.strip("\n").split(",")
                
                gate_a = self.gates[connection[0]]
                gate_b = self.gates[connection[1]]
                draw_x = gate_a["x_coord"]
                draw_y = gate_a["y_coord"]               
                
                while draw_y != gate_b["y_coord"]:
                    # north
                    if draw_y < gate_b["y_coord"]:
                        draw_y = self.wire_north(draw_x, draw_y)
                    # south
                    if draw_y > gate_b["y_coord"]:
                        draw_y = self.wire_south(draw_x, draw_y)

                while draw_x != gate_b["x_coord"]:
                    # east
                    if draw_x < gate_b["x_coord"]:
                        draw_x = self.wire_east(draw_x, draw_y)
                    # west
                    if draw_x > gate_b["x_coord"]:
                        draw_x = self.wire_west(draw_x, draw_y)




    def wire_north(self, draw_x, draw_y):
        self.coordinates[draw_x][draw_y].connections.append("north")
        self.coordinates[draw_x][draw_y + 1].connections.append("south")

        x1 = [draw_x, draw_x]
        y1 = [draw_y, draw_y + 1]
    
        plt.plot(x1, y1, 'r')
        draw_y += 1
        return draw_y

    def wire_east(self, draw_x, draw_y):
        self.coordinates[draw_x][draw_y].connections.append("east")
        self.coordinates[draw_x + 1][draw_y].connections.append("west")

        x1 = [draw_x, draw_x + 1]
        y1 = [draw_y, draw_y]
    
        plt.plot(x1, y1, 'r')
        draw_x += 1
        return draw_x
    
    def wire_south(self, draw_x, draw_y):
        self.coordinates[draw_x][draw_y].connections.append("south")
        self.coordinates[draw_x - 1][draw_y].connections.append("north")

        x1 = [draw_x, draw_x]
        y1 = [draw_y, draw_y - 1]
        
        plt.plot(x1, y1, 'r')
        draw_y -= 1
        return draw_y
        
    def wire_west(self, draw_x, draw_y):
        self.coordinates[draw_x][draw_y].connections.append("west")
        self.coordinates[draw_x - 1][draw_y].connections.append("east")
        
        x1 = [draw_x, draw_x - 1]
        y1 = [draw_y, draw_y]
        
        plt.plot(x1, y1, 'r')
        draw_x -= 1
        return draw_x
    




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
