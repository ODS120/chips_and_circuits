import csv
import random
import os

class Chip():
    def __init__(self, chip_data, netlist):
        self.height = 0
        self.width = 0
        self.depth = 0
        self.coordinates = []
        self.gates = {}

        self.used_nodes = []
        self.total_cost = 0
        self.nr_wires = 0
        self.nr_intersections = 0
        
        self.best_cost = float("inf")
        self.best_nr_wires = 0
        self.best_nr_intersections = 0
        

        with open('output.csv', 'w', newline='') as file:
            output = csv.writer(file)
            output.writerow(["net", "wires"])
        
        # prepare the chip to be worked with
        self.load_grid(chip_data)
        self.load_coordinates()
        self.load_gates()

        with open(netlist) as connections_data:
            next(connections_data)

            # store wires in list
            wires  = []
            for wire_data in connections_data:
                if len(wire_data) < 2:
                    break
                wires.append(wire_data)
        
        wire_id = 0
        open_wires = []
        closed_wires = {}
        for wire in wires:
            connect_gates_id = wire.strip("\n").split(",")
            self.wire_data[wire_id] = {"a": connect_gates_id[0], "b": connect_gates_id[1], "source_node": self.gates[connect_gates_id[0]]['node_object'], "goal_node": self.gates[connect_gates_id[1]]['node_object'], "path": [self.gates[connect_gates_id[0]]['node_object']], "wire_cost": 0, "wire_length": 0}
            # add source node to list with used nodes
            self.used_nodes.append(self.gates[connect_gates_id[0]]['node_object']) 

            open_wires.append(wire_id)
            wire_id += 1

        nr_wires = len(open_wires)
        iteration = 0
        paths_data = []
        total_iterations = 0


        counter = 1
        paths_best_iteration = []
        iterations = 5000

        while open_wires:
            # add wire_id to source node
            if wire_id not in self.wire_data[wire_id]['source_node'].wires:
                self.wire_data[wire_id]['source_node'].wires.append(wire_id)


            # reset all used coordinates and data
            self.total_cost = 0
            self.nr_wires = 0
            self.nr_intersections = 0
            for node in self.used_nodes:
                node.cost = 1
                node.parent = None
                node.closed_neighbours = []

            all_paths = [] 

            if counter % 50 == 0:
                print(counter)
            counter += 1
                      
            random.shuffle(wires)
           
            for wire in wires:
                # draw wire between two gates
                connect_gates_id = wire.strip("\n").split(",")

                # switch start and goal node at half of iterations
                if x < (iterations / 2):
                    source_node = self.gates[connect_gates_id[0]]['node_object']
                    goal_node = self.gates[connect_gates_id[1]]['node_object']
                else: 
                    source_node = self.gates[connect_gates_id[1]]['node_object']
                    goal_node = self.gates[connect_gates_id[0]]['node_object']
                path = self.path_search(source_node, goal_node)

                if path == None:
                    self.total_cost = float("inf")
                    break

                # if costs already higher than best try, go to next iteration
                if self.total_cost > self.best_cost or self.total_cost > 20000:
                    self.total_cost = float("inf")
                    break
                
                # store wires data
                all_paths.append([connect_gates_id[0], connect_gates_id[1], path])

            # if path is better, save new path and best cost data          
            if self.total_cost < self.best_cost:
                self.best_nr_wires = self.nr_wires
                self.best_nr_intersections = self.nr_intersections
                self.best_cost = self.total_cost
                paths_best_iteration = all_paths
                print(f"Best: {self.best_cost}  Nr wires: {self.best_nr_wires}   Nr intersections: {self.best_nr_intersections}  Try: {counter}")
            


        # save the results
        for path_data in paths_best_iteration:
            self.save_csv((path_data[0], path_data[1]), path_data[2])
        
        print(f"Best: {self.best_cost}")  
        # filter id names
        chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
        net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

        with open('dimensions.csv', 'w') as file:
            output = csv.writer(file)
            output.writerow([self.width, self.height, self.depth])
        # Add last line to the file
        with open('output.csv', 'a', newline='') as file:
            output = csv.writer(file)
            output.writerow([f"chip_{chip_id}_net_{net_id}", self.best_cost])



    def path_search (self, source_node, goal_node):
        current_node = source_node
        self.used_nodes.append(source_node)

        path = []
        path.append([source_node.x_coord, source_node.y_coord, source_node.z_coord])
        while current_node != goal_node:
            # change cost of current node
            current_node.cost = 301
            options = []
            for neighbour in current_node.neighbours: 
                # store parent
                if neighbour in current_node.closed_neighbours:
                    continue
                if neighbour.gate and neighbour != goal_node:
                    continue
                    
                neighbour.distance_to_goal = self.calculate_distance_to_goal(neighbour, goal_node)
                neighbour.flat_distance_to_goal = self.calculate_flat_distance_to_goal(neighbour, goal_node)
                neighbour.heuristic = neighbour.distance_to_goal + neighbour.cost + neighbour.near_gate_cost

                options.append(neighbour)      

            if len(options) == 0:
                self.total_cost = float("inf")
                break              

            # sort options on distance to goal
            # options.sort(key=lambda x: (x.distance_to_goal, x.cost, x.flat_distance_to_goal))
            options.sort(key=lambda x: (x.heuristic, x.distance_to_goal, x.flat_distance_to_goal))
            # get best option
            best_option = options.pop(0)

            # close chosen path for other wires
            current_node.closed_neighbours.append(best_option)
            best_option.closed_neighbours.append(current_node)

            # store parent of chosen node
            best_option.parent = current_node

            # add node to path
            path.append([best_option.x_coord, best_option.y_coord, best_option.z_coord])
            self.used_nodes.append(best_option)
            current_node = best_option

            # add cost
            self.total_cost += current_node.cost

            # count intersections
            if current_node.cost == 301:
                self.nr_intersections += 1
            
            # count wires
            self.nr_wires += 1
           
            # return path if goal found
            if best_option == goal_node:
                return path
        return None
        

    
    def calculate_distance_to_goal(self, current_node, goal_node):
        distance = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord) + abs(current_node.z_coord - goal_node.z_coord)
        return distance
    def calculate_flat_distance_to_goal(self, current_node, goal_node):
        distance = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord)
        return distance

    # load the grid
    def load_grid(self, chip_data):
        with open(chip_data) as chip_grid:
            next(chip_grid)

            for line in chip_grid:
                gate_info = line.strip("\n").split(",")
                self.gates[gate_info[0]] = {"x_coord": int(gate_info[1]), "y_coord": int(gate_info[2]), "z_coord": 0, "node_object": None}

                # find the max x and y coordinate
                if int(gate_info[1]) > self.width:
                    self.width = int(gate_info[1])
                if int(gate_info[2]) > self.height:
                    self.height = int(gate_info[2])
            # add borders to the grid
            self.width += 2
            self.height += 2 

     # load all the coordinate classes
    def load_coordinates(self):
        # create 3d grid list with zeroes
        self.coordinates = [[[0 for z in range(8)] for y in range(self.height)] for x in range(self.width)]
        # replace zeroes with node objects
        for x in range(self.width):
            for y in range(self.height):
                for z in range(8):
                    coordinate = Coordinate(x, y, z)
                    self.coordinates[x][y][z] = coordinate

        # get node neighbours for every coordinate
        for x in range(self.width):
            for y in range(self.height):
                for z in range(8):
                    coordinate = self.coordinates[x][y][z]

                    # create x axis neighbours
                    if x + 1 < self.width:
                        coordinate.neighbours.append(self.coordinates[x+1][y][z])
                    if x - 1 >= 0:
                        coordinate.neighbours.append(self.coordinates[x-1][y][z])
                    # create y axis neighbours
                    if y + 1 < self.height:
                        coordinate.neighbours.append(self.coordinates[x][y+1][z])
                    if y - 1 >= 0:
                        coordinate.neighbours.append(self.coordinates[x][y-1][z])
                    # create z axis neighbours
                    if z + 1 < 8:
                        coordinate.neighbours.append(self.coordinates[x][y][z+1])
                    if z - 1 >= 0:
                        coordinate.neighbours.append(self.coordinates[x][y][z-1])


    def load_gates(self):
        for gate_id in self.gates:
            gate_info = self.gates[gate_id]
            # create gate object 
            gate_object = Gate(gate_id, gate_info["x_coord"], gate_info["y_coord"], gate_info["z_coord"], self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]])
            
            self.gates[gate_id]["node_object"] = self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]]
            # print(f"x: {self.gates[gate_id]['node_object'].x_coord} y: {self.gates[gate_id]['node_object'].y_coord}")
            self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]].gate = gate_object
            for gate_neighbour in gate_object.node.neighbours:
                gate_neighbour.near_gate_cost = .5
                for gate_neighbour in gate_object.node.neighbours:
                    gate_neighbour.near_gate_cost = .5
                    for gate_neighbour in gate_object.node.neighbours:
                        gate_neighbour.near_gate_cost = .5
   

    def save_csv(self, net, wires):
        with open('output.csv', 'a', newline='') as results:
            output = csv.writer(results)
            output.writerow([net,wires])


class Coordinate(): 
    def __init__(self, x, y, z):
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z

        self.neighbours = []
        self.closed_neighbours = []

        self.gate = None
        self.cost = 1
        self.near_gate_cost = 0
        self.distance_to_goal = None
        self.flat_distance_to_goal = None
        self.vert_distance_to_goal = None
        self.heuristic = None

        self.parent = None
        self.wires = []

    # Print node
    def __repr__(self):
        return ('({0},{1},{2},{3})'.format(self.distance_to_goal, self.x_coord, self.y_coord, self.z_coord))
                       

class Gate():
    def __init__(self, gate_id, x, y, z, node):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.node = node


