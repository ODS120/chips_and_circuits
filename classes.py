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
                        draw_y = self.wire_north(draw_x, draw_y, "r")
                    # east
                    elif draw_x < gate_b["x_coord"] and "east" not in connect:
                        old_x = draw_x
                        draw_x = self.wire_east(draw_x, draw_y, "r")
                    # west
                    elif draw_x > gate_b["x_coord"] and "west" not in connect:
                        old_x = draw_x
                        draw_x = self.wire_west(draw_x, draw_y, "r")
                    # south
                    elif draw_y > gate_b["y_coord"] and "south" not in connect:
                        old_y = draw_y
                        draw_y = self.wire_south(draw_x, draw_y, "r")
                    else:
                        if draw_y != gate_b["y_coord"] or draw_x != gate_b["x_coord"]:
                            wire_counter -= 2
                            wires.pop()
                            
                            if draw_x != old_x:
                                # east
                                if draw_x < old_x:
                                    draw_x = self.wire_east(draw_x, draw_y, "b")
                                # west
                                elif draw_x > old_x:
                                    draw_x = self.wire_west(draw_x, draw_y, "b")

                                # north
                                if draw_y <= gate_b["y_coord"] and "north" not in connect:
                                    draw_y = self.wire_north(draw_x, draw_y, "r")
                                 # south
                                elif draw_y >= gate_b["y_coord"] and "south" not in connect:
                                    draw_y = self.wire_south(draw_x, draw_y, "r")  

                            elif draw_y != old_y:
                                # north
                                if draw_y < old_y:
                                    draw_y = self.wire_east(draw_x, draw_y, "b")
                                # south
                                elif draw_y > old_y:
                                    draw_x = self.wire_west(draw_x, draw_y, "b")

                                # east
                                if draw_x <= gate_b["x_coord"] and "east" not in connect:
                                    draw_x = self.wire_east(draw_x, draw_y, "r")
                                # west
                                elif draw_x >= gate_b["x_coord"] and "west" not in connect:
                                    draw_x = self.wire_west(draw_x, draw_y, "r")
                        else:
                            break

                    wire_counter += 1
                    if f"({draw_x},{draw_y})" not in wires:
                        wires.append(f"({draw_x},{draw_y})")
            # 

                # print(net,wires)
                self.save_csv(net, f"[{','.join(wires)}]")
                    # # north
                    # elif "north" not in connect:
                    #     draw_y = self.wire_north(draw_x, draw_y)
                    # # south
                    # elif "south" not in connect:
                    #     draw_y = self.wire_south(draw_x, draw_y)
                    # # east
                    # elif "east" not in connect:
                    #     draw_x = self.wire_east(draw_x, draw_y)
                    # # west
                    # elif "west" not in connect:
                    #     draw_x = self.wire_west(draw_x, draw_y)
        return wire_counter, collision_counter


    def wire_north(self, draw_x, draw_y, colour):
        print("NORTH")
        self.coordinates[draw_x][draw_y].connections.append("north")
        self.coordinates[draw_x][draw_y + 1].connections.append("south")

        x1 = [draw_x, draw_x]
        y1 = [draw_y, draw_y + 1]
    
        plt.plot(x1, y1, colour)
        draw_y += 1
        return draw_y

    def wire_east(self, draw_x, draw_y, colour):
        print("EAST")
        self.coordinates[draw_x][draw_y].connections.append("east")
        self.coordinates[draw_x + 1][draw_y].connections.append("west")

        x1 = [draw_x, draw_x + 1]
        y1 = [draw_y, draw_y]
    
        plt.plot(x1, y1, colour)
        draw_x += 1
        # print(draw_x)
        return draw_x
    
    def wire_south(self, draw_x, draw_y, colour):
        print("SOUTH")
        self.coordinates[draw_x][draw_y].connections.append("south")
        self.coordinates[draw_x - 1][draw_y].connections.append("north")

        x1 = [draw_x, draw_x]
        y1 = [draw_y, draw_y - 1]
        
        plt.plot(x1, y1, colour)
        draw_y -= 1
        return draw_y
        
        
    def wire_west(self, draw_x, draw_y, colour):
        print("WEST")
        self.coordinates[draw_x][draw_y].connections.append("west")
        self.coordinates[draw_x - 1][draw_y].connections.append("east")
        
        x1 = [draw_x, draw_x - 1]
        y1 = [draw_y, draw_y]
        
        plt.plot(x1, y1, colour)
        draw_x -= 1
        return draw_x
    
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
