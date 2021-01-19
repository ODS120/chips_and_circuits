import matplotlib.pyplot as plt
import csv
import random
import copy

import os

class Chip():
    def __init__(self, chip_data, netlist):
        self.height = 0
        self.width = 0
        self.depth = 0
        self.coordinates = []
        self.gates = {}
        self.wires = 0
        self.crossroad = [] #open
        self.travelled_path = [] #closed
        self.checked_order = []
        
        # Prepare the chip to be worked with
        self.load_grid(chip_data)
        self.load_connections(netlist)
   
        # Filter id names
        chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
        net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

        with open('dimensions.csv', 'w') as file:
            output = csv.writer(file)
            output.writerow([self.width, self.height, self.depth])

        # Add last line to the file
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([f"chip_{chip_id}_net_{net_id}", self.wires])


    # load the grid
    def load_grid(self, chip_data):
        """
        Create an internal 2d grid on which the case will be represented
        and save the gate positions.

        Args:
            chip_data ([type]): [description]
        """
        with open(chip_data) as chip_grid:
            next(chip_grid)

            for line in chip_grid:
                gate_info = line.strip("\n").split(",")
                self.gates[gate_info[0]] = {"x_coord": int(gate_info[1]), "y_coord": int(gate_info[2])}

                # Find the max x and y coordinate
                if int(gate_info[1]) > self.width:
                    self.width += int(gate_info[1])

                if int(gate_info[2]) > self.height:
                    self.height += int(gate_info[2])
            
            # Add borders to the grid
            self.width += 2
            self.height += 2 


    def load_connections(self, netlist):
        """
        Check the netlist for the way the gates are to be connected and put them
        in random order.

        Args:
            netlist ([type]): [description]
        """
        with open(netlist) as connections:
            # Skip first and last line of netlist file
            next(connections)
            connections = [connect.strip('\n') for connect in connections]
            # del connections[-1]

            restart = True

            while restart:
                restart = False

                # Reset/initiate output file
                with open('output.csv', 'w', newline='') as file:
                    output = csv.writer(file)
                    output.writerow(["net", "wires"])

                # Reset variables
                self.crossroad = []
                self.travelled_path = []
                self.coordinates = []
                self.depth = 0

                # Reset/initiate internal representation
                self.load_coordinates()
                self.load_gates()

                # Manage the visual reprentation of the grid
                plt.xlim([0, self.width - 1])
                plt.ylim([0, self.height - 1])
                # plt.axis('off')

                random.shuffle(connections)

                # Check whether this order has been checked before
                if connections in self.checked_order:
                    continue

                self.checked_order.append(connections)

                # Add end of list signal
                connections.append('')

                print(connections)
                # Iterate through all connections
                for connect in connections:
                    if self.connect_gates(connect):
                        # Remove end of list signal
                        restart = True
                        del connections[-1]
                        break


    def load_coordinates(self):
        """
        Initiate all the coordinate classes of a new layer and add their possible connections

        Args:
            z ([type]): [description]
        """
        for z in range(8):
            # Initiate a pre-filled grid
            self.coordinates.append([[0 for x in range(self.width)] for y in range(self.height)])

            # iterate over all the grid coordinates
            # Iterate through the grid
            for y in range(self.height):
                for x in range(self.width):
                    # Draw 2d representation TODO remove once finished
                    if z == 0 :
                        x1 = [x, x+1]
                        x2 = [x, x]
                        y1 = [y, y]
                        y2 = [y, y+1]
                        plt.plot(x1, y1, 'b', x2, y2, 'b')

                    coordinate = Coordinate(x, y, z)

                    # Add connections
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

                    # Replace coordinate with its respective class
                    self.coordinates[z][y][x] = coordinate


    # load all the gate classes
    def load_gates(self):
        """
        Initiate Gate classes and add them to the internal representation of the grid.
        """        
        for gate_id in self.gates:
            gate = self.gates[gate_id]
            gate_object = Gate(gate_id, gate["x_coord"], gate["y_coord"])

            # plot the gate onto the chip TODO remove when done
            plt.plot(gate["x_coord"], gate["y_coord"], 'ro', marker = "s", markersize = 20)

            # plot gate label TODO remove when done
            plt.annotate(f"{gate_id}", (gate["x_coord"], gate["y_coord"]), fontsize = 13, ha = "center", va = "center")

            # appoint the gate its position on the grid
            self.coordinates[3][gate["y_coord"]][gate["x_coord"]].gate = gate_object


    def connect_gates(self, connect):
        """
        Connect two gates according to the netlist and retrieve its path.

        Args:
            connect ([type]): [description]
            connections ([type]): [description]

        Returns:
            [type]: [description]
        """        
        if connect == '':
            return False

        connect_gates = connect.strip("\n").split(",")
        path = self.move(connect_gates[0], connect_gates[1])

        if path is None:
            return True

        # Draw the wires in 2d plot TODO remove when done
        for wires in range(len(path) - 1):
            self.wires += 1
            self.wire(path[wires], path[wires + 1], "r")

        # File the results
        self.save_csv((connect_gates[0], connect_gates[1]), path)

        # Visualize the solution TODO remove when done
        plt.savefig('test.png')

        return False


    def wire(self, source, goal, colour): #direction
        # Plot 2d TODO Remove when done
        #print(f"source: {source}")
        x = [source[0], goal[0]]
        y = [source[1], goal[1]]
        z = [source[2], goal[2]]
        plt.plot(x, y, colour)
    

    def save_csv(self, net, wires):
        """
        Add a new completed path to the output file

        Args:
            net ([type]): [description]
            wires ([type]): [description]
        """        
        with open('output.csv', 'a', newline='') as results:
            output = csv.writer(results)
            output.writerow([net,wires])
        

    def move(self, source_gate, target_gate):
        """
        Prepare to run the algorithm.

        Args:
            source_gate ([type]): [description]
            target_gate ([type]): [description]

        Returns:
            [type]: [description]
        """      
        self.crossroad = []
        self.travelled_path = []

        # Source and target always on z-axis 0
        source_coords = [self.gates[source_gate]["x_coord"], self.gates[source_gate]["y_coord"], 0]
        target_coords = [self.gates[target_gate]["x_coord"], self.gates[target_gate]["y_coord"], 0]
        
        validity_check = [source_coords, target_coords]

        for gates in validity_check:
            (x, y, z) = gates
            neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z), (x, y, z+1), (x, y, z-1)]

            # Check validity of the coordinates around the gates
            for nodes in neighbours:
                if nodes[2] < 0:
                    return None

                # TODO Waar was deze ook al weer voor?
                elif self.coordinates[nodes[2]][nodes[1]][nodes[0]].cost < 300:
                    break
                
                elif nodes == (x, y, z-1):
                    return None

        self.calculate_distance(target_coords)

        start_node = Node(source_coords, None, 0)
        goal_node = Node(target_coords, None, 0)

        self.crossroad.append(start_node)

        return self.run_algorithm(source_coords, target_coords, start_node, goal_node)


    def run_algorithm(self, source_coords, target_coords, start_node, goal_node):
        """
        Run the algorithm.

        Args:
            source_coords ([type]): [description]
            target_coords ([type]): [description]
            start_node ([type]): [description]
            goal_node ([type]): [description]

        Returns:
            [type]: [description]
        """
        while len(self.crossroad) > 0:
            self.crossroad.sort()

            # Retrieve the node with the lowest cost
            current_node = self.crossroad.pop(0)

            self.travelled_path.append(current_node)

            # Check whether the the goal has been reached, return the path
            if current_node == goal_node:

                return self.retrace_path(current_node, start_node, goal_node, source_coords)

            (x, y, z) = current_node.position

            neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z), (x, y, z+1), (x, y, z-1)]
            self.calculate_distance(target_coords)

            for next_door in neighbours:
                self.check_directions(next_door, current_node, goal_node)

        return self.retrace_path(current_node, start_node, goal_node, source_coords)


    def retrace_path(self, current_node, start_node, goal_node, source_coords):
        """
        Retrieve the taken path from one gate to another, from goal to start.

        Args:
            current_node ([type]): [description]
            start_node ([type]): [description]
            goal_node ([type]): [description]
            source_coords ([type]): [description]

        Returns:
            [type]: [description]
        """        
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

            if current_node != goal_node and current_node != start_node:
                self.coordinates[z][y][x].cost = 300

            path.append(current_node.position)
            current_node = current_node.parent

        path.append(source_coords)

        # Reverse the order of the path
        return path[::-1]


    def check_directions(self, next_door, current_node, goal_node):
        """
        Check one of the nodes next to the current node.

        Args:
            next_door ([type]): [description]
            current_node ([type]): [description]
            goal_node ([type]): [description]
            target_coords ([type]): [description]
        """        
        if next_door[2] < 0 or next_door[2] >= 8:
            return

        # Check if the node is off the grid
        if next_door[0] < 0 or next_door[0] > self.width - 1 or next_door[1] < 0 or next_door[1] > self.height - 1:
            return

        (x, y, z) = current_node.position

        # Check whether a connection is already being used
        if self.coordinates[z][y][x].connections[next_door].used:
            return

        next_node = self.coordinates[next_door[2]][next_door[1]][next_door[0]]

        # Create a neighbor node
        neighbour = Node(next_door, current_node, next_node.cost + next_node.distance_to_goal)

        if neighbour != goal_node and self.coordinates[next_door[2]][next_door[1]][next_door[0]].gate is not None:
            return

        # Check if the neighbor is in the closed list
        if neighbour in self.travelled_path:
            return
        
        # Check if neighbor is in open list and if it has a lower cost value
        if(self.add_to_open(neighbour, goal_node)):
            self.crossroad.append(neighbour)


    def calculate_distance(self, target_coords):
        """
        Calculate the distance to the goal ffrom all the coordinates.

        Args:
            target_coords ([type]): [description]
        """        
        # print(f"target: {target_coords}")
        # print(f"target x: {target_coords[0]}")
        for z in self.coordinates:
            # print(f"z: {z}")
            for y in z:
                try:
                    for x in y:
                        x.distance_to_goal = abs(x.x_coord - target_coords[0])
                        x.distance_to_goal += abs(x.y_coord - target_coords[1])
                        x.distance_to_goal += abs(x.z_coord - target_coords[2])
                except AttributeError:
                    # print(z)
                    # print(self.width)
                    # print(self.height)
                    # print(self.depth)
                    # print(f"len: {test for test in self.coordinates}")
                    x.distance_to_goal = abs(x.x_coord - target_coords[0])
                
                    # print(x.x_coord, x.y_coord, x.z_coord)
                    # print(x.distance_to_goal)


    # Check if a neighbor should be added to open list
    def add_to_open(self, neighbour, goal_node):
        """ Check to see of the node is a valid option to research.

        Args:
            neighbour ([type]): [description]
            goal_node ([type]): [description]

        Returns:
            [type]: [description]
        """        
        for node in self.crossroad:
            if node.cost <= neighbour.cost and node != goal_node:
                return False
        
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

        # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.cost))


class Coordinate(): 
    def __init__(self, x, y, z):
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.gate = None
        # north, east, south, west, up, down
        self.connections = {}
        self.cost = 1
        self.distance_to_goal = 0 


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
