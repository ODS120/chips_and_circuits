import matplotlib.pyplot as plt
import csv

import os

class Chip():
    def __init__(self, chip_data, netlist):
        self.height = 0
        self.width = 0
        self.depth = 0
        self.coordinates = []
        self.gates = {}
        self.wires = 0

        with open('output.csv', 'w', newline='') as file:
            output = csv.writer(file)
            output.writerow(["net", "wires"])
        
        # Prepare the chip to be worked with
        self.load_grid(chip_data)
        self.load_coordinates(0)
        self.load_gates()

        # Manage the visual reprentation of the grid
        plt.xlim([0, self.width - 1])
        plt.ylim([0, self.height - 1])
        plt.axis('off')

        with open(netlist) as connections:
            next(connections)

            # Iterate seperately through all connections
            for line in connections:
                connect_gates = line.strip("\n").split(",")

                # Connect two gates
                path = self.move(connect_gates[0], connect_gates[1])
                print(path)
                # Draw the wires
                for wires in range(len(path) - 1):
                    self.wires += 1
                    self.wire(path[wires], path[wires + 1], "r")
                
                # File the results
                self.save_csv((connect_gates[0], connect_gates[1]), path)

                # Visualize the solution
                plt.savefig('test.png')
    
        # Filter id names
        chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
        net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

        # Add last line to the file
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([f"chip_{chip_id}_net_{net_id}", self.wires])


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


    # load all the coordinate classes
    def load_coordinates(self, z):
        # fill the grid
        self.coordinates.append([[0 for x in range(self.width)] for y in range(self.height)])
        
        # iterate over all the grid coordinates
        # TODO draai de x en y waarde om, nu is verwarrend
        for y in range(self.height):
            for x in range(self.width):
                x1 = [x, x+1]
                x2 = [x, x]
                y1 = [y, y]
                y2 = [y, y+1]
                plt.plot(x1, y1, 'b', x2, y2, 'b')

                coordinate = Coordinate(x, y, z)

                if z > 0:
                    coordinate.connections[x, y, z - 1] = Wire(x, y, z - 1)
                    self.coordinates[z-1][y][x].connections[x, y, z] = Wire(x, y, z)

                if y >= 0 and y < self.height:
                    coordinate.connections[x, y + 1, z] = Wire(x, y + 1, z)

                if y > 0 and y <= self.height:
                    coordinate.connections[x, y - 1, z] = Wire(x, y - 1, z)

                if x >= 0 and x < self.width:
                    coordinate.connections[x + 1, y, z] = Wire(x + 1, y, z)

                if x > 0 and x <= self.width:
                    coordinate.connections[x - 1, y, z] = Wire(x - 1, y, z)
                
                self.coordinates[z][y][x] = coordinate


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
            self.coordinates[0][gate["y_coord"]][gate["x_coord"]].gate = gate_object


    def wire(self, source, goal, colour): #direction
        #print(f"source: {source}")
        x = [source[0], goal[0]]
        y = [source[1], goal[1]]
        z = [source[2], goal[2]]
        plt.plot(x, y, colour)
    

    def save_csv(self, net, wires):
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([net,wires])


    def move(self, source_gate, target_gate):
        crossroad = [] #open
        travelled_path = [] #closed

        # Source and target always on z-axis 0
        source_coords = [self.gates[source_gate]["x_coord"], self.gates[source_gate]["y_coord"], 0]
        target_coords = [self.gates[target_gate]["x_coord"], self.gates[target_gate]["y_coord"], 0]

        start_node = Node(source_coords, None, 300)
        goal_node = Node(target_coords, None, 300)

        crossroad.append(start_node)

        while len(crossroad) > 0:
            # crossroad.sort()
            current_node = crossroad.pop(0)
            travelled_path.append(current_node)

            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path = []

                # TODO Dit kan hoogstwaarschijnlijk handiger worden geschreven
                while current_node != start_node:
                    x = current_node.position[0]
                    y = current_node.position[1]
                    z = current_node.position[2]
                    parent_coords = current_node.parent.position
                    # set wire between coordinates
                    self.coordinates[z][y][x].connections[parent_coords[0], parent_coords[1], parent_coords[2]].used = True
                    self.coordinates[parent_coords[2]][parent_coords[1]][parent_coords[0]].connections[x, y, z].used = True
                    self.coordinates[z][y][x].cost = 300

                    path.append(current_node.position)
                    current_node = current_node.parent

                path.append(source_coords) 

                # Return reversed path
                return path[::-1]

            # print(self.coordinates[z][y][x].connections[parent_coords[0], parent_coords[1], parent_coords[2]])

            (x, y, z) = current_node.position

            neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z), (x, y, z+1), (x, y, z-1)]

             # Loop neighbours
            for next_door in neighbours:
                if next_door[2] < 0:
                    continue

                if next_door[2] > self.depth:
                    self.depth += 1
                    self.load_coordinates(next_door[2])

                # Check if the node is off the grid
                if next_door[0] < 0 or next_door[0] > self.width - 1 or next_door[1] < 0 or next_door[1] > self.height - 1:
                    continue

                # Check whether a connection is already being used
                if self.coordinates[z][y][x].connections[next_door].used:
                    continue

                # Create a neighbor node
                neighbour = Node(next_door, current_node, self.coordinates[next_door[2]][next_door[1]][next_door[0]].cost)

                if neighbour != goal_node and self.coordinates[next_door[2]][next_door[1]][next_door[0]].gate != None:
                    continue

                # Check if the neighbor is in the closed list
                if neighbour in travelled_path:
                    continue

                # Check if neighbor is in open list and if it has a lower cost value
                if(self.add_to_open(crossroad, neighbour, goal_node) == True):
                    # Everything is green, add neighbor to open list
                    crossroad.append(neighbour)
        
        path = []
        # Return None, no path is found
        while current_node != start_node:
            print("test")
            x = current_node.position[0]
            y = current_node.position[1]
            z = current_node.position[2]
            parent_coords = current_node.parent.position
            # set wire between coordinates
            self.coordinates[z][y][x].connections[parent_coords[0], parent_coords[1], parent_coords[2]].used = True
            self.coordinates[parent_coords[2]][parent_coords[1]][parent_coords[0]].connections[x, y, z].used = True
            self.coordinates[z][y][x].cost = 300

            path.append(current_node.position)
            current_node = current_node.parent

        path.append(source_coords) 

        # Return reversed path
        return path[::-1]
        # return None


    # Check if a neighbor should be added to open list
    def add_to_open(self, crossroad, neighbour, goal_node):
        for node in crossroad:
            pass
            # if (neighbour.cost == 300 and neighbour != goal_node):
            #     return False

        return True


class Node():
    def __init__(self, position, parent, cost):
        self.position = [position[0], position[1], position[2]]
        self.parent = parent
        self.cost = cost
    
    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
         return self.cost < other.cost


class Coordinate(): 
    def __init__(self, x, y, z):
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.gate = None
        # north, east, south, west, up, down
        self.connections = {}
        self.cost = 1   


class Gate():
    def __init__(self, gate_id, x, y):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y


class Wire():
    # stores wire found by algorithm 
    def __init__(self, x, y, z):
        # self.wire_id = wire_id
        self.x = x
        self.y = y
        self.z = z
        self.used = False
        self.total_cost = 0

    def add_wire(self, to_node, cost):
        pass
        # stores node objects
        # self.nodes.append(to_node)
        # self.total_cost += cost
