'''
Hill Climber algorithm explanation
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
        chip_data ([type]): [description]
        netlist ([type]): [description]
    """
    # isolate file digits
    chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
    net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

    chip = cp.Chip(chip_data, netlist)

    open_wires = transform_data_input(chip, netlist)

    run_algorithm(chip, open_wires)
    generate_output(chip, chip_id, net_id)


def transform_data_input(chip, netlist):
    """
    Check the netlist for the way the gates are to be connected and store data.

    Args:
        chip_data ([type]): [description]
        netlist ([type]): [description]
    
    Returns:
        open_wires [type]: [description]
    """
    # open file
    with open('output.csv', 'w', newline='') as file:
        output = csv.writer(file)
        output.writerow(["net", "wires"])

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
    for wire in wires:
        connect_gates_id = wire.strip("\n").split(",")
        chip.wire_data[wire_id] = {"source_gate": connect_gates_id[0], "goal_gate": connect_gates_id[1], "source_node": chip.gates[connect_gates_id[0]]['node_object'], "goal_node": chip.gates[connect_gates_id[1]]['node_object'], "path": [chip.gates[connect_gates_id[0]]['node_object']], "wire_cost": 0, "wire_length": 0}
        open_wires.append(wire_id)
        wire_id += 1
    return open_wires


def run_algorithm(chip, open_wires):
    """
    Run Hill Climber the algorithm.

    Args:
        chip ([type]): [description]
        open_wires ([type]): [description]
    """   

    nr_wires = len(open_wires)
    total_resets = 0
    iteration = 0
    closed_wires = {}
    tries = 100

    # loop over wires and draw
    while open_wires:
        for wire_id in open_wires:
            # add wire_id to source node wires
            if wire_id not in chip.wire_data[wire_id]['source_node'].wire_ids:
                chip.wire_data[wire_id]['source_node'].wire_ids.append(wire_id)

            # search path for wire
            wire_path = path_search(chip, chip.wire_data[wire_id]['source_node'], chip.wire_data[wire_id]['goal_node'], wire_id)

            # if wiring couldn't find path, add to closed_wires with infinite cost
            if wire_path == False:
                open_wires.remove(wire_id) 
                chip.wire_data[wire_id]['wire_cost'] = float("inf")
                closed_wires[wire_id] = chip.wire_data[wire_id]['wire_cost']
                break
            
            # remove wire from open_wires and add to closed_wires
            open_wires.remove(wire_id) 
            closed_wires[wire_id] = chip.wire_data[wire_id]['wire_cost']

        # if no wires to draw, calculate total costs
        if len(open_wires) == 0:
            # calculate total cost and length
            total_cost = 0
            total_length = 0
            for wire_id in closed_wires:
                total_cost += chip.wire_data[wire_id]['wire_cost']
                total_length += chip.wire_data[wire_id]['wire_length']

            # if netlist improved, store paths of wires
            if total_cost < chip.best_cost:
                chip.best_cost = total_cost
                chip.best_length = total_length
                print(f"IMPROVED Total cost: {chip.best_cost}  Total length: {chip.best_length}  Iteration: {iteration}  Resets: {total_resets}")

                chip.best_paths_data = []
                # save best path in right format
                for wire_id in closed_wires:
                    path_coordinates = []
                    for node in chip.wire_data[wire_id]['path']:
                        path_coordinates.append((node.x_coord, node.y_coord, node.z_coord))
                    chip.best_paths_data.append([chip.wire_data[wire_id]['source_gate'], chip.wire_data[wire_id]['goal_gate'], path_coordinates])

            # remove wires, add wire_id to open_wires and clean coordinates
            if total_resets < tries: 
                iteration += 1

                # sort wires on cost 
                sorted_wires = sorted(closed_wires.items(), key=lambda x: x[1])
                
                # get wires to redraw
                remove_wires = sorted_wires[iteration:]

                # if all wires are infinite or iterated over every wire, reset all wires
                if sorted_wires[0][1] == float("inf") or iteration == nr_wires:
                    total_resets += 1
                    iteration = 0
                    remove_wires = list(closed_wires.items()) 
                    
                    if (total_resets % (total_resets/100)) == 0:
                        print(f"Resets: {total_resets}")
                        print("_____")
                open_wires = remove_wires_algorithm(chip, open_wires, closed_wires, remove_wires)

            
def path_search(chip, source_node, goal_node, wire_id):
    """
    Run path search algorithm

    Args:
        chip ([type]): [description]
        source_node ([type]): [description]
        goal_node ([type]): [description]
        wire_id ([type]): [description]
    
    Returns:
        [Bool]: [description]
    """   
    
    current_node = source_node
    node_counter = []

    while current_node != goal_node:
        # change cost of current node
        current_node.cost = 301
        options = [] 
        # loop over all neighbours
        for neighbour in current_node.neighbours:    
            if neighbour == goal_node:

                # close chosen path for other wires, store parent of node and add wire_id to node
                current_node.closed_neighbours.append(goal_node)
                goal_node.closed_neighbours.append(current_node)
                goal_node.parent = current_node
                goal_node.wire_ids.append(wire_id)

                # add node to path, cost and wire length of wire
                chip.wire_data[wire_id]['path'].append(goal_node)
                chip.wire_data[wire_id]['wire_cost'] += 1
                chip.wire_data[wire_id]['wire_length'] += 1
                return True

            if neighbour in current_node.closed_neighbours:
                continue
            if neighbour.gate and neighbour != goal_node:
                continue

            neighbour.distance_to_goal = calculate_distance_to_goal(neighbour, goal_node)
            neighbour.heuristic = neighbour.distance_to_goal + neighbour.cost
            options.append(neighbour)      

        # return if no options available
        if len(options) == 0:
            return False          

        # sort options on heuristic and get lowest heuristic node
        options.sort(key=lambda x: (x.heuristic))
        lowest_heuristic_node = options[0]

        # get comparable options
        comparable_options = []
        for option in options:
            if option.heuristic == lowest_heuristic_node.heuristic:
                comparable_options.append(option)
        best_option = random.choice(comparable_options)
        
        # close chosen path for other wires, store parent of node and add wire_id to node
        current_node.closed_neighbours.append(best_option)
        best_option.closed_neighbours.append(current_node)
        best_option.parent = current_node 
        best_option.wire_ids.append(wire_id)
    
        # add node to path, cost and wire length of wire
        chip.wire_data[wire_id]['path'].append(best_option)
        chip.wire_data[wire_id]['wire_cost'] += best_option.cost
        chip.wire_data[wire_id]['wire_length'] += 1
        
        # return path if goal found
        if best_option == goal_node:
            return True
        current_node = best_option
    return None


def remove_wires_algorithm(chip, open_wires, closed_wires, remove_wires):     
    """
    Run path search algorithm

    Args:
        chip ([type]): [description]
        open_wires ([type]): [description]
        closed_wires ([type]): [description]
        remove_wires ([type]): [description]
    
    Returns:
       open_wires [type]: [description]
    """              
    # iterate over wires and reset paths and data
    for wire in remove_wires:
        wire_id = wire[0]

        # add wire_id to open wires and remove wire from closed wires
        open_wires.append(wire_id)
        del closed_wires[wire_id]

        # reset wire cost and length
        chip.wire_data[wire_id]['wire_cost'] = 0
        chip.wire_data[wire_id]['wire_length'] = 0                       

        # iterate over nodes of wire path
        for node in chip.wire_data[wire_id]['path']:
            # remove wire_id from coordinate
            if wire_id in node.wire_ids:
                node.wire_ids.remove(wire_id)

            # open path
            if node.parent:
                if node.parent in node.closed_neighbours:
                    node.closed_neighbours.remove(node.parent)
                if node in node.parent.closed_neighbours:
                    node.parent.closed_neighbours.remove(node)

            # if node intersection is free, change node costs back to default
            if len(node.wire_ids) == 0:
                node.cost = 1
        chip.wire_data[wire_id]['path'] = [chip.wire_data[wire_id]['source_node']]

    # shuffle order of open_wires to be drawn
    random.shuffle(open_wires)
    # swap start and end of wire
    for wire_id in open_wires:
        temp = chip.wire_data[wire_id]['source_node']
        chip.wire_data[wire_id]['source_node'] = chip.wire_data[wire_id]['goal_node']
        chip.wire_data[wire_id]['goal_node'] = temp   
        chip.wire_data[wire_id]['path'] = [chip.wire_data[wire_id]['source_node']]
    
    # return wires to redraw
    return open_wires


def calculate_distance_to_goal(current_node, goal_node):
    """
    Run path search algorithm

    Args:
        current_node ([type]): [description]
        goal_node ([type]): [description]
    
    Returns:
       distance [type]: [description]
    """    
    distance = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord) + abs(current_node.z_coord - goal_node.z_coord)
    return distance


def generate_output(chip, chip_id, net_id):
    """
    Run path search algorithm

    Args:
        chip ([type]): [description]
        chip_id ([type]): [description]
        net_id ([type]): [description]
    
    Returns:
        csv [type]: [description]
    """    
    
    print("FINISH")
    # save results
    for path_data in chip.best_paths_data:
        print(path_data)
        
        save_csv((path_data[0], path_data[1]), path_data[2])
    print(f"Best cost: {chip.best_cost} ")            
    
    with open('dimensions.csv', 'w') as file:
        output = csv.writer(file)
        output.writerow([chip.width, chip.height, chip.depth])
    # add last line to the file
    with open('output.csv', 'a', newline='') as file:
        output = csv.writer(file)
        output.writerow([f"chip_{chip_id}_net_{net_id}", chip.best_cost]) 


def save_csv(net, wires):
    """
    Run path search algorithm

    Args:
        net ([type]): [description]
        wires ([type]): [description]
    
    Returns:
        csv [type]: [description]
    """   

    with open('output.csv', 'a', newline='') as results:
        output = csv.writer(results)
        output.writerow([net,wires])


