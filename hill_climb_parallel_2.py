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
        self.wire_paths = {}

        self.best_cost = float("inf")
        self.best_length = 0


        with open('output.csv', 'w', newline='') as file:
            output = csv.writer(file)
            output.writerow(["net", "wires"])
        
        # prepare the chip to be worked with
        self.load_grid(chip_data)
        self.load_coordinates()
        self.load_gates()

        # load netlist data
        with open(netlist) as connections_data:
            next(connections_data)
            # store wires in list
            wires  = []
            for wire_data in connections_data:
                if len(wire_data) < 2:
                    break
                wires.append(wire_data)

        # create dictionary  wire_id: wire data
        wire_id = 0
        open_wires = []
        closed_wires = {}
        for wire in wires:
            connect_gates_id = wire.strip("\n").split(",")
            self.wire_paths[wire_id] = {"a": connect_gates_id[0], "b": connect_gates_id[1], "source_node": self.gates[connect_gates_id[0]]['node_object'], "goal_node": self.gates[connect_gates_id[1]]['node_object'], "path": [self.gates[connect_gates_id[0]]['node_object']], "wire_cost": 0, "wire_length": 0}
            # add source node to list with used nodes
            self.used_nodes.append(self.gates[connect_gates_id[0]]['node_object']) 

            open_wires.append(wire_id)
            wire_id += 1

        nr_wires = len(open_wires)
        iteration = 0
        paths_data = []
        total_iterations = 0
        # loop over wires and draw
        while open_wires:
            for wire_id in open_wires:  
                # add wire_id to source node
                if wire_id not in self.wire_paths[wire_id]['source_node'].wires:
                    self.wire_paths[wire_id]['source_node'].wires.append(wire_id)

                # calculate next step
                current_location = self.path_search(self.wire_paths[wire_id]['path'][-1], self.wire_paths[wire_id]['goal_node'], wire_id)

                # if wiring couldn't finish, remove wire id and add infinite wire cost
                if current_location == None:
                    self.wire_paths[wire_id]['wire_cost'] = float("inf")
                    open_wires.remove(wire_id) 
                    closed_wires[wire_id] = self.wire_paths[wire_id]['wire_cost']
                    break
                
                # add wire_id to node
                current_location.wires.append(wire_id)
                # add node to list with used nodes
                self.used_nodes.append(current_location) 
                # add new node to wire's path 
                self.wire_paths[wire_id]['path'].append(current_location)

                # check if location is wire's goal
                if self.wire_paths[wire_id]['goal_node'] == current_location:
                    open_wires.remove(wire_id) 
                    closed_wires[wire_id] = self.wire_paths[wire_id]['wire_cost']


            # if no wires to draw, calculate total costs
            if len(open_wires) == 0:
                # calculate total cost and length
                total_cost = 0
                total_length = 0
                for wire_id in closed_wires:
                    total_cost += self.wire_paths[wire_id]['wire_cost']
                    total_length += self.wire_paths[wire_id]['wire_length']

                # if netlist improved, store paths of wires
                if total_cost < self.best_cost:
                    print("IMRPOVED")
                    self.best_cost = total_cost
                    self.best_length = total_length
                    print(f"Total cost: {self.best_cost}  Total length: {self.best_length}")
                    paths_data = []
                    for wire_id in closed_wires:
                        path_coordinates = []
                        for node in self.wire_paths[wire_id]['path']:
                            path_coordinates.append([node.x_coord, node.y_coord, node.z_coord])
                        paths_data.append([self.wire_paths[wire_id]['a'], self.wire_paths[wire_id]['b'], path_coordinates])

                # remove wires, add wire_id to open_list and clean coordinates
                if iteration != nr_wires:
                    total_iterations += 1
                    iteration += 1

                    if total_iterations % 50 == 0:
                        print(f"Try: {total_iterations}")
                        
                    # sort wires on cost 
                    sorted_wires = sorted(closed_wires.items(), key=lambda x: x[1])
                    
                    # get wires to redraw
                    remove_wires = sorted_wires[iteration:]
              
                    # if no solution found, restart with new start wire order
                    if iteration == nr_wires and total_iterations < 700:
                        iteration = 0
                        remove_wires = list(closed_wires.items()) 

                    # iterate over wires and remove
                    for wire in remove_wires:
                        # add wire_id to open wires
                        open_wires.append(wire[0])

                        # reset wire cost and length
                        self.wire_paths[wire[0]]['wire_cost'] = 0
                        self.wire_paths[wire[0]]['wire_length'] = 0

                        # remove wire from closed wires
                        del closed_wires[wire[0]]

                        # iterate over nodes of wire path
                        for node in self.wire_paths[wire[0]]['path']:

                            # remove wire_id from coordinate
                            if wire[0] in node.wires:
                                node.wires.remove(wire[0])

                            # open path
                            if node.parent in node.closed_neighbours:
                                node.closed_neighbours.remove(node.parent)
                                node.parent.closed_neighbours.remove(node)
                            
                            # if node intersection is free, change node costs
                            if len(node.wires) == 0:
                                node.cost = 1
                    # shuffle order of wires to redraw
                    random.shuffle(open_wires)
                

        print("FINISH")
        # save results
        for path_data in paths_data:
            print(path_data)
            
            self.save_csv((path_data[0], path_data[1]), path_data[2])
        print(f"Best cost: {self.best_cost} ")            
        
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




                
    def path_search (self, current_node, goal_node, wire_id):
        options = []

        for neighbour in current_node.neighbours: 
            # pick best neigbour
            if neighbour in current_node.closed_neighbours:
                continue
            if neighbour.gate and neighbour != goal_node:
                continue

            if neighbour == goal_node:
                self.used_nodes.append(goal_node)

                # close chosen path for other wires
                current_node.closed_neighbours.append(neighbour)
                neighbour.closed_neighbours.append(current_node)

                # store parent of chosen node
                neighbour.parent = current_node

                # add wire length
                self.wire_paths[wire_id]['wire_length'] += 1
                self.wire_paths[wire_id]['wire_cost'] += 1
                
                neighbour.cost = 300
                current_node.cost = 300
                return neighbour
            
            neighbour.distance_to_goal = self.calculate_distance_to_goal(neighbour, goal_node)
            neighbour.flat_distance_to_goal = self.calculate_flat_distance_to_goal(neighbour, goal_node)
            neighbour.vertic_distance_to_goal = self.calculate_flat_distance_to_goal(neighbour, goal_node)
            

            neighbour.heuristic = neighbour.cost + neighbour.distance_to_goal + neighbour.near_gate_cost
            options.append(neighbour)      

        if len(options) == 0:
            return None   

        # sort options on distance to goal
        options.sort(key=lambda x: (x.heuristic, x.flat_distance_to_goal))

        # get best option
        best_option = options.pop(0)
        
        # close chosen path for other wires
        current_node.closed_neighbours.append(best_option)
        best_option.closed_neighbours.append(current_node)

        # store parent of chosen node
        best_option.parent = current_node
              
        # add cost
        if best_option.cost == 300:
            self.wire_paths[wire_id]['wire_cost'] += 300
        else: 
            self.wire_paths[wire_id]['wire_cost'] += 1

        # add wire length
        self.wire_paths[wire_id]['wire_length'] += 1

        # change nodes cost
        best_option.cost = 300
        current_node.cost = 300

        return best_option




    def calculate_distance_to_goal(self, current_node, goal_node):
        distance = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord) + abs(current_node.z_coord - goal_node.z_coord)
        return distance
    def calculate_flat_distance_to_goal(self, current_node, goal_node):
        distance = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord)
        return distance
    def calculate_vertic_distance_to_goal(self, current_node, goal_node):
        distance = abs(current_node.y_coord - goal_node.y_coord)
        return distance



    # load the grid
    def load_grid(self, chip_data):
        with open(chip_data) as chip_grid:
            next(chip_grid)

            for line in chip_grid:
                gate_info = line.strip("\n").split(",")
                self.gates[gate_info[0]] = {"x_coord": int(gate_info[1]), "y_coord": int(gate_info[2]), "z_coord": 3, "node_object": None,  }

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
            self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]].cost = 1

            for gate_neighbour in gate_object.node.neighbours:
                gate_neighbour.near_gate_cost = .5
                # for gate_neighbour in gate_neighbour.neighbours:
                #     gate_neighbour.near_gate_cost = .5
                #     for gate_neighbour in gate_neighbour.neighbours:
                #         gate_neighbour.near_gate_cost = .1

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
        self.heuristic = None

        self.parent = None
        self.wires = []

    # Print node
    def __repr__(self):
        # return ('({0},{1},{2},{3})'.format(self.distance_to_goal, self.x_coord, self.y_coord, self.z_coord))
        return ('({0},{1},{2})'.format(self.x_coord, self.y_coord, self.z_coord))
                       

class Gate():
    def __init__(self, gate_id, x, y, z, node):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.node = node