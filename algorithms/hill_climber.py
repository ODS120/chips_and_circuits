'''
Jan-Joost Raedts, Olaf Stringer, Martijn van Veen,

Hill Climber based algorithm 
'''

import csv
import random
import os

from classes_hill_climber import chip as cp
from classes_hill_climber import gate as gt
from classes_hill_climber import coordinate as crd
        

def main(chip_data, netlist):
    """
    Implicates a hill climber algorithm.

    Args:
        chip_data (file): The coordinates of the gates
        netlist (file): The way the gates are to be connected
    """
    # Isolate file digits for output
    chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
    net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

    # Initiate Chip class
    chip = cp.Chip(chip_data, netlist)
    open_paths = transform_data_input(chip, netlist)

    # Run algoritm and generate output
    run_algorithm(chip, open_paths)
    generate_output(chip, chip_id, net_id)


def transform_data_input(chip, netlist):
    """
    Checks the netlist for the way the gates are to be connected and stores the path data as a dictionary.
    Creates list with path IDs to be connected.

    Args:
        chip (object): Internal representation of the chip
        netlist (file): The way the gates are to be connected
    
    Returns:
        open_paths (list): The path id's that need to be connected
    """
    # Create CSV file for output data
    with open('output.csv', 'w', newline='') as file:
        output = csv.writer(file)
        output.writerow(["net", "wires"])

    # Load netlist data and store paths in list
    with open(netlist) as connections_data:
        next(connections_data)
        paths  = []
        for path_data in connections_data:
            if len(path_data) < 2:
                break
            paths.append(path_data)

    # Create dictionaries with path data and store in list
    path_id = 0
    open_paths = []
    for path in paths:
        connect_gates_id = path.strip("\n").split(",")
        chip.path_data[path_id] = {"source_gate": connect_gates_id[0], "goal_gate": connect_gates_id[1], "source_node": chip.gates[connect_gates_id[0]]['node_object'], "goal_node": chip.gates[connect_gates_id[1]]['node_object'], "path": [chip.gates[connect_gates_id[0]]['node_object']], "path_cost": 0, "path_length": 0}
        open_paths.append(path_id)
        path_id += 1
    return open_paths


def run_algorithm(chip, open_paths):
    """
    Run the Hill Climber algorithm.

    Args:
        chip (object): Internal representation of the chip
        open_paths (list): The path id's that need to be connected
    """   

    nr_paths = len(open_paths)
    total_resets = 0
    iteration = 0
    closed_paths = {}
    tries = 100

    # Find path for every open path
    while open_paths:
        for path_id in open_paths:
            # Add path_id to source node's path_ids; the paths that make use of this specific node
            if path_id not in chip.path_data[path_id]['source_node'].path_ids:
                chip.path_data[path_id]['source_node'].path_ids.append(path_id)

            # Find route for path_id
            path_route = path_search(chip, chip.path_data[path_id]['source_node'], chip.path_data[path_id]['goal_node'], path_id)

            # If algorithm couldn't find route, add path_id to closed_paths with an infinite cost
            if path_route == False:
                open_paths.remove(path_id) 
                chip.path_data[path_id]['path_cost'] = float("inf")
                closed_paths[path_id] = chip.path_data[path_id]['path_cost']
                break
            
            # If route found succesfully, remove path_id from open_paths and 
            # add path_id to closed_paths dictionary; path_id:path_cost
            open_paths.remove(path_id) 
            closed_paths[path_id] = chip.path_data[path_id]['path_cost']

        # If no paths to route, calculate total costs
        if len(open_paths) == 0:
            # Calculate total cost and length of all paths together
            total_cost = 0
            total_length = 0
            for path_id in closed_paths:
                total_cost += chip.path_data[path_id]['path_cost']
                total_length += chip.path_data[path_id]['path_length']

            # If total cost improved, store paths data
            if total_cost < chip.best_cost:
                chip.best_cost = total_cost
                chip.best_length = total_length
                print(f"Total cost: {chip.best_cost}  Total length: {chip.best_length}  Iteration: {iteration}  Resets: {total_resets}")
                chip.best_paths_data = []

                # Save best path in right format for CSV output
                for path_id in closed_paths:
                    path_coordinates = []
                    for node in chip.path_data[path_id]['path']:
                        path_coordinates.append((node.x_coord, node.y_coord, node.z_coord))
                    chip.best_paths_data.append([chip.path_data[path_id]['source_gate'], chip.path_data[path_id]['goal_gate'], path_coordinates])

            # Remove routed paths to reroute
            if total_resets < tries: 
                iteration += 1

                # Sort paths on cost and get most expensive paths to reroute
                sorted_paths = sorted(closed_paths.items(), key=lambda x: x[1])
                remove_paths = sorted_paths[iteration:]

                # If best path has infinite cost or algorithm iterated over every path; reroute all paths
                if sorted_paths[0][1] == float("inf") or iteration == nr_paths:
                    total_resets += 1
                    iteration = 0
                    remove_paths = list(closed_paths.items()) 
                    
                    if (total_resets % (total_resets/10)) == 0:
                        print(f"Resets: {total_resets}")
                        print("_____")
                # Remove paths and add path_ids to open_paths to reroute
                open_paths = remove_paths_algorithm(chip, open_paths, closed_paths, remove_paths)

            
def path_search(chip, source_node, goal_node, path_id):
    """
    Runs path search algorithm

    Args:
        chip (object): Internal representation of the chip
        source_node (object): Coordinate-object of the start node
        goal_node (object): Coordinate-object of the goal node
        path_id (int): ID which can be used to get all data of a specific path
    
    Returns:
        (bool): Returns true if a path was found succesfully
    """   
    current_node = source_node
    node_counter = []

    while current_node != goal_node:
        # Change cost of current node and set step options to 0
        current_node.cost = 301
        options = [] 
        # Loop over all neighbour nodes of current node
        for neighbour in current_node.neighbours:    
            if neighbour == goal_node:
                # Close chosen path for other routes and store parent of node
                current_node.closed_neighbours.append(goal_node)
                goal_node.closed_neighbours.append(current_node)
                goal_node.parent = current_node
                # Add path_id to node's path_ids; the paths that make use of this specific node
                goal_node.path_ids.append(path_id)

                # Add step, cost and path length to path
                chip.path_data[path_id]['path'].append(goal_node)
                chip.path_data[path_id]['path_cost'] += 1
                chip.path_data[path_id]['path_length'] += 1
                return True

            # Skip neighbour node if it's not allowed to take that step
            if neighbour in current_node.closed_neighbours:
                continue
            if neighbour.gate and neighbour != goal_node:
                continue

            # Calculate heuristic of neighbour node and append node to step options
            neighbour.distance_to_goal = calculate_distance_to_goal(neighbour, goal_node)
            neighbour.heuristic = neighbour.distance_to_goal + neighbour.cost + neighbour.near_gate_cost
            options.append(neighbour)      

        # Return false routing if no step options available
        if len(options) == 0:
            return False          

        # Sort options on heuristic and get lowest heuristic node
        options.sort(key=lambda x: (x.heuristic))
        lowest_heuristic_node = options[0]

        # Get options with the same heuristic value and pick random option
        comparable_options = []
        for option in options:
            if option.heuristic == lowest_heuristic_node.heuristic:
                comparable_options.append(option)
        best_option = random.choice(comparable_options)
        
        # Close chosen step for other paths, store parent of node
        current_node.closed_neighbours.append(best_option)
        best_option.closed_neighbours.append(current_node)
        best_option.parent = current_node 
        # Add path_id to node's path_ids; the paths that make use of this specific node
        best_option.path_ids.append(path_id)
    
        # Add step to path, add cost and path length
        chip.path_data[path_id]['path'].append(best_option)
        chip.path_data[path_id]['path_cost'] += best_option.cost
        chip.path_data[path_id]['path_length'] += 1
        
        # Return path if goal found
        if best_option == goal_node:
            return True
        current_node = best_option
    return None


def remove_paths_algorithm(chip, open_paths, closed_paths, remove_paths):     
    """
    Removes routed paths from chip

    Args:
        chip (object): Internal representation of the chip
        open_paths (list): The path id's that need to be routed
        closed_paths (list): The path id's that have been connected
        remove_paths (list): The paths that need to be removed
    
    Returns:
       open_paths list: The path id's that need to be (re)connected
    """              
    # Iterate over path_ids to remove path
    for path in remove_paths:
        path_id = path[0]

        # Add path_id to open paths and remove path_id from closed paths
        open_paths.append(path_id)
        del closed_paths[path_id]

        # Reset path cost and length
        chip.path_data[path_id]['path_cost'] = 0
        chip.path_data[path_id]['path_length'] = 0                       

        # Iterate over nodes of the path and clean path data
        for node in chip.path_data[path_id]['path']:
            # Remove path_id from coordinate's path_ids; the paths that make use of this specific node
            if path_id in node.path_ids:
                node.path_ids.remove(path_id)

            # Remove closed step option from coordinate node
            if node.parent:
                if node.parent in node.closed_neighbours:
                    node.closed_neighbours.remove(node.parent)
                if node in node.parent.closed_neighbours:
                    node.parent.closed_neighbours.remove(node)

            # If node intersection is free, change node costs back to default
            if len(node.path_ids) == 0:
                node.cost = 1
        chip.path_data[path_id]['path'] = [chip.path_data[path_id]['source_node']]

    # Shuffle order of open_paths to be routed and swap start and end of paths
    random.shuffle(open_paths)
    for path_id in open_paths:
        temp = chip.path_data[path_id]['source_node']
        chip.path_data[path_id]['source_node'] = chip.path_data[path_id]['goal_node']
        chip.path_data[path_id]['goal_node'] = temp   
        chip.path_data[path_id]['path'] = [chip.path_data[path_id]['source_node']]
    
    # Return paths to reroute
    return open_paths


def calculate_distance_to_goal(current_node, goal_node):
    """
    Calculates distance between nodes

    Args:
        current_node (object): Coordinate-object of the current node
        goal_node (object): Coordinate-object of the goal node
    
    Returns:
       distance (int): Distance between current and goal node
    """    
    distance = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord) + abs(current_node.z_coord - goal_node.z_coord)
    return distance


def generate_output(chip, chip_id, net_id):
    """
    Generates output in CSV format

    Args:
        chip (object): Internal representation of the chip
        chip_id (int): Chip number
        net_id (int): Netlist number
    """    

    print("FINISH")
    # Loop over stored paths and save in CSV file
    for path_data in chip.best_paths_data:
        print(path_data)
        
        # store path source, goal and path_nodes in CSV output file
        with open('output.csv', 'a', newline='') as results:
            output = csv.writer(results)
            output.writerow([(path_data[0], path_data[1]), path_data[2]])

    print(f"Best cost: {chip.best_cost} ")            
    
    # Create dimensions CSV file used for visualization 
    with open('dimensions.csv', 'w') as file:
        output = csv.writer(file)
        output.writerow([chip.width, chip.height, chip.depth])

    # Add chip_id, net_id and chip_cost to CSV output file
    with open('output.csv', 'a', newline='') as file:
        output = csv.writer(file)
        output.writerow([f"chip_{chip_id}_net_{net_id}", chip.best_cost]) 



