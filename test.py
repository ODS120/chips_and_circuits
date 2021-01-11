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
        # self.plot_chip()
        self.load_coordinates()
        self.load_gates()

        with open(netlist) as connections:
            next(connections)

            for line in connections:
                print("gate")
                connect_gates = line.strip("\n").split(",")
                path = self.move(connect_gates[0], connect_gates[1])
                #print(path)
                for wires in range(len(path) - 1):
                    self.wire(path[wires], path[wires + 1], "r")
                
                plt.xlim([0, self.width - 1])
                plt.ylim([0, self.height - 1])
                plt.legend()
                plt.xticks([])
                plt.yticks([])
                plt.axis('off')
                plt.show()
                plt.savefig('test.png')
        
        # self.
        # # total_cost 
        # n, k = self.draw_wires(netlist)
        # print(n)
        # # costs 
        # cost = n + 300 * k
        # print(cost)

        plt.xlim([0, self.width - 1])
        plt.ylim([0, self.height - 1])
        # plt.legend()
        # plt.xticks([])
        # plt.yticks([])
        # plt.axis('off')
        plt.show()
        plt.savefig('test.png')
        cost = 0
        chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
        net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")
        print(chip_id, net_id)
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([f"chip_{chip_id}_net_{net_id}", cost])


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


    # def plot_chip(self):
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             x1 = [x, x+1]
    #             x2 = [x, x]
    #             y1 = [y, y]
    #             y2 = [y, y+1]
    #             plt.plot(x1, y1, 'b', x2, y2, 'b')


    # load all the coordinate classes
    def load_coordinates(self):
        # iterate over all the grid coordinates
        for y in range(self.height):
            for x in range(self.width):
                x1 = [x, x+1]
                x2 = [x, x]
                y1 = [y, y]
                y2 = [y, y+1]
                plt.plot(x1, y1, 'b', x2, y2, 'b')

                coordinate = Coordinate(x, y)

                if y >= 0 and y < self.height:
                    coordinate.connections[x, y + 1] = Wire(x, y + 1)

                if y > 0 and y <= self.height:
                    coordinate.connections[x, y - 1] = Wire(x, y - 1)

                if x >= 0 and x < self.width:
                    coordinate.connections[x + 1, y] = Wire(x + 1, y)

                if x > 0 and x <= self.width:
                    coordinate.connections[x - 1, y] = Wire(x - 1, y)
                
                self.coordinates[y][x] = coordinate

        print(self.coordinates[0][0].connections)
        print(self.width)
        print(self.height)


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
                        
                        # if draw_x != old_x:
                        #     # remove wire
                        #     # east
                        #     if draw_x < old_x:
                        #         draw_x = self.wire_east(draw_x, draw_y, "b")
                        #     # west
                        #     elif draw_x > old_x:
                        #         draw_x = self.wire_west(draw_x, draw_y, "b")

                        #     # north
                        #     if draw_y <= gate_b["y_coord"] and "north" not in connect:
                        #         draw_y = self.wire_north(draw_x, draw_y, "r")
                        #     # south
                        #     elif draw_y >= gate_b["y_coord"] and "south" not in connect:
                        #         draw_y = self.wire_south(draw_x, draw_y, "r")  

                        # elif draw_y != old_y:
                        #     # remove wire
                        #     # north
                        #     if draw_y < old_y:
                        #         draw_y = self.wire_east(draw_x, draw_y, "b")
                        #     # south
                        #     elif draw_y > old_y:
                        #         draw_x = self.wire_west(draw_x, draw_y, "b")
                        #     # east
                        #     if draw_x <= gate_b["x_coord"] and "east" not in connect:
                        #         draw_x = self.wire_east(draw_x, draw_y, "r")
                        #     # west
                        #     elif draw_x >= gate_b["x_coord"] and "west" not in connect:
                        #         draw_x = self.wire_west(draw_x, draw_y, "r")
                        # else:
                        break

                    wire_counter += 1
                    if f"({draw_x},{draw_y})" not in wires:
                        wires.append(f"({draw_x},{draw_y})")

                # print(net,wires)
                self.save_csv(net, f"[{','.join(wires)}]")
        return wire_counter, collision_counter


    def wire(self, source, goal, colour): #direction
        #print(f"source: {source}")
        x1 = [source[0], goal[0]]
        y1 = [source[1], goal[1]]
        plt.plot(x1, y1, colour)

        # draw_x = 0
        # draw_y = 0
        # direction = "nope"
        # # add direction to current coordinate
        # self.coordinates[draw_x][draw_y].connections.append(direction)

        # if direction == "north" or direction == "south":
        #     # hold the x-coordinates of the line
        #     x1 = [draw_x, draw_x]

        #     # calculate a line to the north
        #     if direction == "north":
        #         self.coordinates[draw_x][draw_y + 1].connections.append("south")
        #         y1 = [draw_y, draw_y + 1]
        #         draw_y += 1
        #     # calculate a line to the south
        #     else:
        #         self.coordinates[draw_x][draw_y - 1].connections.append("north")
        #         y1 = [draw_y, draw_y - 1]
        #         draw_y -= 1
        
        # elif direction == "east" or direction == "west":
        #     # hold the y-coordinates of the line
        #     y1 = [draw_y, draw_y]

        #     # calculate a line to the east
        #     if direction == "east":
        #         self.coordinates[draw_x + 1][draw_y].connections.append("west")
        #         x1 = [draw_x + 1, draw_x]
        #         draw_x += 1
        #     # calculate a line to the west
        #     else:
        #         self.coordinates[draw_x - 1][draw_y].connections.append("east")
        #         x1 = [draw_x - 1, draw_x]
        #         draw_x -= 1

        # draw the line        
        # plt.plot(x1, y1, colour)
        # print(colour)

        # return current position on the grid
        # return draw_x, draw_y
    

# (1,2),"[(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]"
    def save_csv(self, net, wires):
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([net,wires])


    def move(self, source_gate, target_gate):
        
        crossroad = [] #open
        travelled_path = [] #closed
        source_coords = [self.gates[source_gate]["x_coord"], self.gates[source_gate]["y_coord"]]
        target_coords = [self.gates[target_gate]["x_coord"], self.gates[target_gate]["y_coord"]]

        start_node = Node(source_coords, None)
        goal_node = Node(target_coords, None)

        crossroad.append(start_node)

        while len(crossroad) > 0:
            crossroad.sort()
            current_node = crossroad.pop(0)

            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    print(f"postition:{current_node.position}")
                    x = current_node.position[0]
                    y = current_node.position[1]
                    coords = current_node.parent.position
                    print(coords[0], coords[1])
                    # print(self.coordinates[y][x].connections)
                    # print(self.coordinates[y][x].connections[coords[0], coords[1]].used)
                    self.coordinates[y][x].connections[coords[0], coords[1]].used = True
                    print(self.coordinates[coords[0]][coords[1]].connections)
                    self.coordinates[coords[1]][coords[0]].connections[x, y].used = True
                    # print(self.coordinates[y][x].connections[coords[0], coords[1]].used)
                    path.append(current_node.position)
                    current_node = current_node.parent

                path.append(source_coords) 
                # Return reversed path
                return path[::-1]

            (x, y) = current_node.position

            neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

             # Loop neighbours
            for next_door in neighbours:
                print(x, y)
                print(f"next: {next_door}")
                # Check if the node is of the grid
                if next_door[0] < 0 or next_door[0] > self.width - 1 or next_door[1] < 0 or next_door[1] > self.height - 1:
                    print("test1")
                    continue

                if self.coordinates[y][x].connections[next_door].used:
                    print("test2")
                    print(self.coordinates[y][x].connections)
                    print(self.coordinates[y][x].connections[next_door])
                    continue

                # Create a neighbor node
                neighbour = Node(next_door, current_node)
                
                # Check if the neighbor is in the closed list
                if neighbour in travelled_path:
                    print("test3")
                    continue

                # Generate heuristics (Manhattan distance)
                neighbour.cost += 1 

                # Check if neighbor is in open list and if it has a lower cost value
                if(self.add_to_open(crossroad, neighbour) == True):
                    # Everything is green, add neighbor to open list
                    crossroad.append(neighbour)
        # Return None, no path is found
        return None


    # Check if a neighbor should be added to open list
    def add_to_open(self, crossroad, neighbour):
        for node in crossroad:
            if (neighbour == node and neighbour.cost >= node.cost):
                return False

        return True


class Node():
    def __init__(self, position, parent):
        self.position = [position[0], position[1]]
        self.parent = parent
        self.cost = 0
    
    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position
    # Sort nodes
    def __lt__(self, other):
         return self.cost < other.cost


class Coordinate(): 
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.gate = []
        # north, east, south, west, up, down
        self.connections = {}   


class Gate():
    def __init__(self, gate_id, x, y):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y

class Wire():
    # stores wire found by algorithm 
    def __init__(self, x, y):
        # self.wire_id = wire_id
        self.x = x
        self.y = y
        self.used = False
        
        self.total_cost = 0

    def add_wire(self, to_node, cost):
        pass
        # stores node objects
        # self.nodes.append(to_node)
        # self.total_cost += cost
