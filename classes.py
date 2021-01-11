import matplotlib.pyplot as plt
import csv

import os

class Chip():
    def __init__(self, chip_data, netlist):
        self.height = 0
        self.width = 0
        self.coordinates = []
        self.gates = {}

        with open('output.csv', 'w', newline='') as file:
            output = csv.writer(file)
            output.writerow(["net", "wires"])
            
        self.load_grid(chip_data)
        self.plot_chip()
        self.load_coordinates()
        self.load_gates()
        # total_cost 
        n, k = self.draw_wires(netlist)
        print(n)
        # costs 
        cost = n + 300 * k
        print(cost)

        chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
        net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")
        print(chip_id, net_id)
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([f"chip_{chip_id}_net_{net_id}", cost])

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
        wire_counter = 0
        collision_counter = 0

        with open(file) as netlist:
            next(netlist)
            
            for line in netlist:
                connection = line.strip("\n").split(",")
                print(connection[0])
                gate_a = self.gates[connection[0]]
                gate_b = self.gates[connection[1]]
                # gate_a = self.gates["1"]
                # gate_b = self.gates["2"]
                draw_x = gate_a["x_coord"]
                draw_y = gate_a["y_coord"]     
                old_x = draw_x
                old_y = draw_y

                net = f"({connection[0]},{connection[1]})"
                wires = []
                wires.append(f"({draw_x},{draw_y})")

                while draw_y != gate_b["y_coord"] or draw_x != gate_b["x_coord"]:
                    # print(f"x coord {draw_x != gate_b['x_coord']}")
                    # print(f"y coord {draw_y != gate_b['y_coord']}")
                    # print(draw_x)
                    # print(gate_b['x_coord'])
                    
                    connect = self.coordinates[draw_x][draw_y].connections
                    # north
                    if draw_y < gate_b["y_coord"] and "north" not in connect:
                        old_y = draw_y
                        draw_x, draw_y = self.wire(draw_x, draw_y, "r", "north")
                    # east
                    elif draw_x < gate_b["x_coord"] and "east" not in connect:
                        old_x = draw_x
                        draw_x, draw_y = self.wire(draw_x, draw_y, "r", "east")
                    # west
                    elif draw_x > gate_b["x_coord"] and "west" not in connect:
                        old_x = draw_x
                        draw_x, draw_y = self.wire(draw_x, draw_y, "r", "west")
                    # south
                    elif draw_y > gate_b["y_coord"] and "south" not in connect:
                        old_y = draw_y
                        draw_x, draw_y = self.wire(draw_x, draw_y, "r", "south")
                    
                    # remove the previously placed wire and use a different route
                    else:
                        wire_counter -= 2
                        wires.pop()
                        
                        if draw_x != old_x:
                            # remove wire
                            # east
                            if draw_x < old_x:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "b", "east")
                            # west
                            elif draw_x > old_x:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "b", "west")

                            # north
                            if draw_y <= gate_b["y_coord"] and "north" not in connect:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "r", "north")
                            # south
                            elif draw_y >= gate_b["y_coord"] and "south" not in connect:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "r", "south")  

                        elif draw_y != old_y:
                            # remove wire
                            # north
                            if draw_y < old_y:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "b", "north")
                            # south
                            elif draw_y > old_y:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "b", "south")
                            # east
                            if draw_x <= gate_b["x_coord"] and "east" not in connect:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "r", "east")
                            # west
                            elif draw_x >= gate_b["x_coord"] and "west" not in connect:
                                draw_x, draw_y = self.wire(draw_x, draw_y, "r", "west")
                        else:
                            break

                    wire_counter += 1
                    if f"({draw_x},{draw_y})" not in wires:
                        wires.append(f"({draw_x},{draw_y})")

                # print(net,wires)
                self.save_csv(net, f"[{','.join(wires)}]")
        return wire_counter, collision_counter


    def wire(self, draw_x, draw_y, colour, direction):
        # add direction to current coordinate
        self.coordinates[draw_x][draw_y].connections.append(direction)

        if direction == "north" or direction == "south":
            # hold the x-coordinates of the line
            x1 = [draw_x, draw_x]

            # calculate a line to the north
            if direction == "north":
                self.coordinates[draw_x][draw_y + 1].connections.append("south")
                y1 = [draw_y, draw_y + 1]
                draw_y += 1
            # calculate a line to the south
            else:
                self.coordinates[draw_x][draw_y - 1].connections.append("north")
                y1 = [draw_y, draw_y - 1]
                draw_y -= 1
        
        elif direction == "east" or direction == "west":
            # hold the y-coordinates of the line
            y1 = [draw_y, draw_y]

            # calculate a line to the east
            if direction == "east":
                self.coordinates[draw_x + 1][draw_y].connections.append("west")
                x1 = [draw_x + 1, draw_x]
                draw_x += 1
            # calculate a line to the west
            else:
                self.coordinates[draw_x - 1][draw_y].connections.append("east")
                x1 = [draw_x - 1, draw_x]
                draw_x -= 1

        # draw the line        
        plt.plot(x1, y1, colour)
        print(colour)

        # return current position on the grid
        return draw_x, draw_y
       
    
# (1,2),"[(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]"
    def save_csv(self, net, wires):
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([net,wires])
            

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

class Wire(): 
    def __init__(self, wire_id, start_node):
        self.wire_id = wire_id
        self.start_node = start_node
        self.nodes = []
        self.total_cost = 0

    def add_wire(self, to_node, cost):
        # stores node objects
        self.nodes.append(to_node)
        self.total_cost += cost

