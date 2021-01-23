'''
A*.py


'''
import csv
import random
import copy
import os
import matplotlib.pyplot as plt

from classes import coordinate as crd
from classes import gate as gt
from classes import node as nd
from classes import wire as wr
from classes import chip as cp


def main(chip_data, netlist):
    """
    Implicates an A* algorithm.

    Args:
        chip_data ([type]): [description]
        netlist ([type]): [description]
    """
    # Isolate file digits
    chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
    net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

    chip = cp.Chip(chip_data, netlist)
    load_connections(netlist, chip, chip_id, net_id)

    with open('dimensions.csv', 'w') as file:
        output = csv.writer(file)
        output.writerow([chip.width, chip.height, chip.depth])


def load_connections(netlist, chip, chip_id, net_id):
    """
    Check the netlist for the way the gates are to be connected and put them
    in random order.

    Args:
        netlist ([type]): [description]
    """
    load_coordinates(chip)
    load_gates(chip)

    with open(netlist) as connections:
        # Skip first and last line of netlist file
        next(connections)

        connections = [connect.strip('\n') for connect in connections]
        # checked_order = []
        min_cost = 0

        # TODO check inbouwen voor compleetheid verbindingen
        # Iterate 10 times
        for i in range(4):
            if i == 1 or i == 3:
                connections = connections[::-1]

            if i == 2:
                length_order = {}

                for connect in connections:
                    order = connect.strip("\n").split(",")
                    source_coords = [chip.gates[order[0]]["x"], chip.gates[order[0]]["y"], 0]
                    target_coords = [chip.gates[order[1]]["x"], chip.gates[order[1]]["y"], 0]

                    gate_dif = abs(source_coords[0] - target_coords[0]) + abs(source_coords[1] - target_coords[1])

                    while gate_dif in length_order:
                        gate_dif += .1

                    length_order[gate_dif] = connect
                
                test = sorted(length_order)
                connections = [length_order[key] for key in test]

            print(i)

            # Reset/initiate variables
            total_path = []
            connected_gates = []
            chip.coordinates = []
            chip.cost = 0

            # Reset/initiate internal representation
            load_coordinates(chip)
            load_gates(chip)

            # Manage the visual reprentation of the grid
            plt.xlim([0, chip.width - 1])
            plt.ylim([0, chip.height - 1])
            # plt.axis('off')

            # random.shuffle(connections)

            # # Check whether this order has been checked before
            # if "".join(connections) in checked_order:
            #     continue

            # checked_order.append("".join(connections))

            # Add end-of-list signal
            connections.append('')
            finished = True

            for connect in connections:
                # Stop when cost are higher than the cheapest iteration
                if chip.cost >= min_cost and min_cost != 0:
                    break

                connect = connect.strip("\n").split(",")

                path, restart, cost, chip = connect_gates(chip, connect)

                if restart:
                    break

                if not path:
                    finished = False

                # Remember succesful connection
                chip.cost += cost

                total_path.append(path)
                connected_gates.append((int(connect[0]), int(connect[1])))

            # Remove end-of-list signal
            del connections[-1]

            # Check for the cheapest iteration
            if (min_cost == 0 or chip.cost < min_cost) and finished:
                min_cost = chip.cost

                save_csv(connected_gates, total_path, net_id, chip_id, chip)


def load_coordinates(chip):
    """
    Initiate all the coordinate classes of a new layer and add their possible connections

    Args:
        z ([type]): [description]
    """
    for z in range(8):
        # Initiate a pre-filled grid
        chip.coordinates.append([[0 for x in range(chip.width)] for y in range(chip.height)])

        # Iterate through the grid
        for y in range(chip.height):
            for x in range(chip.width):
                # Draw 2d representation TODO remove once finished
                if z == 0 :
                    x1 = [x, x+1]
                    x2 = [x, x]
                    y1 = [y, y]
                    y2 = [y, y+1]
                    plt.plot(x1, y1, 'b', x2, y2, 'b')

                coordinate = crd.Coordinate(x, y, z)

                # Add connections
                if z > 0:
                    coordinate.connections[x, y, z - 1] = wr.Wire(x, y, z - 1)
                    chip.coordinates[z-1][y][x].connections[x, y, z] = wr.Wire(x, y, z)

                if y >= 0 and y < chip.height:
                    coordinate.connections[x, y + 1, z] = wr.Wire(x, y + 1, z)

                if y > 0 and y <= chip.height:
                    coordinate.connections[x, y - 1, z] = wr.Wire(x, y - 1, z)

                if x >= 0 and x < chip.width:
                    coordinate.connections[x + 1, y, z] = wr.Wire(x + 1, y, z)

                if x > 0 and x <= chip.width:
                    coordinate.connections[x - 1, y, z] = wr.Wire(x - 1, y, z)

                # Replace coordinate with its respective class
                chip.coordinates[z][y][x] = coordinate


def load_gates(chip):
    """
    Initiate Gate classes and add them to the internal representation of the grid.
    """
    for gate_id in chip.gates:
        gate_coord = chip.gates[gate_id]
        gate = gt.Gate(gate_id, gate_coord["x"], gate_coord["y"])

        # plot the gate onto the chip TODO remove when done
        plt.plot(gate_coord["x"], gate_coord["y"], 'ro', marker = "s", markersize = 20)

        # plot gate label TODO remove when done
        plt.annotate(f"{gate_id}", (gate_coord["x"], gate_coord["y"]), fontsize = 13, ha = "center", va = "center")

        # appoint the gate its position on the grid
        chip.coordinates[0][gate_coord["y"]][gate_coord["x"]].gate = gate


def connect_gates(chip, connect):
    """
    Connect two gates according to the netlist and retrieve its path.

    Args:
        connect ([type]): [description]
        connections ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Reached end of list
    if connect[0] == '':
        return None, True, None, chip

    path, cost, chip = move(chip, connect[0], connect[1])

    # Gates are not connectable
    if path is None:
        return path, True, cost, chip

    # Draw the wires in 2d plot TODO remove when done
    for wires in range(len(path) - 1):
        wire(path[wires], path[wires + 1], "r")

    # Visualize the solution TODO remove when done
    plt.savefig('test.png')

    return path, False, cost, chip


def wire(source, goal, colour): #direction
    # Plot 2d TODO Remove when done
    x = [source[0], goal[0]]
    y = [source[1], goal[1]]
    z = [source[2], goal[2]]
    plt.plot(x, y, colour)


def save_csv(net, wires, net_id, chip_id, chip):
    """
    Save the cheapest cost grid as a csv file.

    Args:
        net ([type]): [description]
        wires ([type]): [description]
    """
    with open(f'output{net_id}.csv', 'w') as file:
        output = csv.writer(file)
        output.writerow(["net", "wires"])

        for step in range(len(wires)):
            output.writerow([net[step],wires[step]])

        output.writerow([f"chip_{chip_id}_net_{net_id}", chip.cost])


def move(chip, source_gate, target_gate):
    """
    Prepare to run the algorithm.

    Args:
        source_gate ([type]): [description]
        target_gate ([type]): [description]

    Returns:
        [type]: [description]
    """      
    crossroad = []
    travelled_path = []

    # Source and target always on z-axis 3
    source_coords = [chip.gates[source_gate]["x"], chip.gates[source_gate]["y"], 0]
    target_coords = [chip.gates[target_gate]["x"], chip.gates[target_gate]["y"], 0]
    
    # validity_check = [source_coords, target_coords]

    # for gates in validity_check:
    #     (x, y, z) = gates
    #     neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z), (x, y, z+1), (x, y, z-1)]

    #     # Check validity of the coordinates around the gates
    #     for nodes in neighbours:
    #         if nodes[2] < 0 or nodes[2] >= 8:
    #             return None

            # # TODO Waar was deze ook al weer voor?
            # elif chip.coordinates[nodes[2]][nodes[1]][nodes[0]].cost < 300:
            #     break

            # elif nodes == (x, y, z-1):
            #     return None

    chip = calculate_distance(target_coords, chip)

    start_node = nd.Node(source_coords, None, 1, 0)
    goal_node = nd.Node(target_coords, None, 1, 0)
    crossroad.append(start_node)

    return run_algorithm(source_coords, target_coords, start_node, goal_node, chip, crossroad, travelled_path)


def run_algorithm(source_coords, target_coords, start_node, goal_node, chip, crossroad, travelled_path):
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
    cheapest_path = []
    cheapest_path_cost = 0
    retrace = False

    while len(crossroad) > 0:
        crossroad.sort()

        # Retrieve the node with the lowest cost
        current_node = crossroad.pop(0)

        if retrace:
            retrace = False

            while current_node.parent != travelled_path[-1]:
                del travelled_path[-1]

                if not travelled_path:
                    break

        travelled_path.append(current_node)

        # Check whether the the goal has been reached, return the path
        if current_node == goal_node:
            
            path, cost, retrace = retrace_path(current_node, start_node, goal_node, source_coords, chip)

            if cost < cheapest_path_cost or cheapest_path_cost == 0:
                cheapest_path = copy.deepcopy(path)
                cheapest_path_cost = cost

        (x, y, z) = current_node.position

        neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z), (x, y, z+1), (x, y, z-1)]
        chip = calculate_distance(target_coords, chip)

        for next_door in neighbours:
            crossroad = check_directions(next_door, current_node, goal_node, chip, crossroad, travelled_path)

    final_path = []
    
    for node in cheapest_path:
        x = node.position[0]
        y = node.position[1]
        z = node.position[2]

        final_path.append(node.position)

        if node == start_node:
            continue
        
        parent_coords = node.parent.position

        # set wire between coordinates
        chip.coordinates[z][y][x].connections[parent_coords[0], parent_coords[1], parent_coords[2]].used = True
        chip.coordinates[parent_coords[2]][parent_coords[1]][parent_coords[0]].connections[x, y, z].used = True

        if node != goal_node:
            chip.coordinates[z][y][x].cost = 301

    return final_path, cheapest_path_cost, chip


def retrace_path(current_node, start_node, goal_node, source_coords, chip):
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
    path_cost = 0

    # TODO Dit kan hoogstwaarschijnlijk handiger worden geschreven
    while current_node != start_node:
        path_cost += current_node.cost

        # x = current_node.position[0]
        # y = current_node.position[1]
        # z = current_node.position[2]
        # parent_coords = current_node.parent.position

        # # set wire between coordinates
        # chip.coordinates[z][y][x].connections[parent_coords[0], parent_coords[1], parent_coords[2]].used = True
        # chip.coordinates[parent_coords[2]][parent_coords[1]][parent_coords[0]].connections[x, y, z].used = True

        # if current_node != goal_node and current_node != start_node:
        #     chip.coordinates[z][y][x].cost = 301

        path.append(current_node)
        current_node = current_node.parent

    path.append(current_node)

    # chip.cost += 1

    # Reverse the order of the path
    return path[::-1], path_cost, True


def check_directions(next_door, current_node, goal_node, chip, crossroad, travelled_path):
    """
    Check one of the nodes next to the current node.

    Args:
        next_door ([type]): [description]
        current_node ([type]): [description]
        goal_node ([type]): [description]
        target_coords ([type]): [description]
    """        
    if next_door[2] < 0 or next_door[2] > 7:
        return crossroad

    # Check if the node is off the grid
    if next_door[0] < 0 or next_door[0] > chip.width - 1 or next_door[1] < 0 or next_door[1] > chip.height - 1:
        return crossroad

    (x, y, z) = current_node.position

    # Check whether a connection is already being used
    if chip.coordinates[z][y][x].connections[next_door].used:
        return crossroad

    next_node = chip.coordinates[next_door[2]][next_door[1]][next_door[0]]

    # Create a neighbor node
    neighbour = nd.Node(next_door, current_node, next_node.cost, next_node.cost + next_node.distance_to_goal)

    if neighbour != goal_node and chip.coordinates[next_door[2]][next_door[1]][next_door[0]].gate is not None:
        return crossroad

    # Check if the neighbor is in the closed list
    if neighbour in travelled_path:
        return crossroad
    
    # Check if neighbor is in open list and if it has a lower cost value
    if (add_to_open(neighbour, goal_node, crossroad)):
        crossroad.append(neighbour)
    
    return crossroad


def calculate_distance(target_coords, chip):
    """
    Calculate the distance to the goal ffrom all the coordinates.

    Args:
        target_coords ([type]): [description]
    """        

    for z in chip.coordinates:
        for y in z:
            for x in y:
                x.distance_to_goal = abs(x.x_coord - target_coords[0])
                x.distance_to_goal += abs(x.y_coord - target_coords[1])
                x.distance_to_goal += abs(x.z_coord - target_coords[2])

    return chip


# Check if a neighbor should be added to open list
def add_to_open(neighbour, goal_node, crossroad):
    """ Check to see of the node is a valid option to research.

    Args:
        neighbour ([type]): [description]
        goal_node ([type]): [description]

    Returns:
        [type]: [description]
    """        
    for node in crossroad:
        if neighbour.heuristic > node.heuristic:
            return False
    
    return True