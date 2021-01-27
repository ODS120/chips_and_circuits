'''
best_first.py TODO

Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Implement a best first algorithm.
'''
import csv
import copy
import os
import time

from classes_best_first import coordinate as crd
from classes_best_first import gate as gt
from classes_best_first import node as nd
from classes_best_first import wire as wr
from classes_best_first import chip as cp


def main(chip_data, netlist):
    """
    Implicates an A* algorithm. TODO

    Args:
        chip_data (file): The coordinates of the gates
        netlist (file): The way the gates are to be connected
    """
    # Start timer
    start = time.perf_counter()

    # Isolate file digits
    chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
    net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

    # Initiate Chip class
    chip = cp.Chip(chip_data, netlist)
    load_connections(netlist, chip, chip_id, net_id)

    end = time.perf_counter()
    print(f"Runtime in seconds: {end - start}")


def load_connections(netlist, chip, chip_id, net_id):
    """
    Check the netlist for the way the gates are to be connected and put them
    in random order.

    Args:
        netlist (file): The way the gates are to be connected
        chip (object): Internal representation of the chip
        chip_id (int): ID to identify the current chip
        net_id ([type]): ID to identify the current netlist
    """
    connections = []

    with open(netlist) as connections:
        # Skip first line of netlist file
        next(connections)
        connections = [connect.strip('\n') for connect in connections]

    save_connections = copy.deepcopy(connections)
    min_cost = 0
    malfunction = []
    reshuffle = False
    order = 0
    attempt = 0

    # Attempt 4 different connection orders
    while order in range(4):
        if reshuffle:
            error_gates = malfunction.pop(0)
            connections, attempt, order = reshuffle_connections(attempt, connections, error_gates, order)
            reshuffle = False
        else:
            attempt = 0
            connections = alter_connection_order(save_connections, order, chip)

        order += 1

        # Reset/initiate variables
        total_path = []
        connected_gates = []
        chip.coordinates = []
        chip.cost = 0
        chip.collisions = 0

        # Reset/initiate internal representation
        chip = load_coordinates(chip)
        chip = load_gates(chip)

        # Add end-of-list signal
        connections.append('')
        finished = True

        for connect in connections:
            # Stop when cost are higher than the cheapest iteration
            if chip.cost >= min_cost and min_cost != 0:
                break

            # Reached end of list
            if connect == '':
                break

            clean_coords = connect.strip("\n").split(",")
            path, cost, chip = prepare_gates(chip, clean_coords[0], clean_coords[1])

            # Gates are not connectable
            if path is None or not path:
                order -= 1
                finished = False
                reshuffle = True
                malfunction.append(connect)
                break

            # Remember succesful connection
            chip.cost += cost
            total_path.append(path)
            connected_gates.append((int(clean_coords[0]), int(clean_coords[1])))

        # Remove end-of-list signal
        del connections[-1]

        # Check for the cheapest iteration
        if (min_cost == 0 or chip.cost < min_cost) and finished:
            min_cost = chip.cost
            save_csv(connected_gates, total_path, net_id, chip_id, chip)


def reshuffle_connections(attempt, connections, error_gates, order):
    """
    Reshuffle the currently ordered connection list so that the
    hindering connection are placed in front.

    Args:
        attempt (int): How often one connection order has been reshuffled
        connections (list): The way the gates will be connected, after shuffle
        error_gates (int): The two gates which could not be connected

    Returns:
        connections (list): The way the gates had to be connected, prior to error
        attempt (int): How often one connection order has been reshuffled
    """
    # No more than 10 attempt to reshuffle
    if attempt > 9:
        attempt = 0
        order += 1

        return connections, attempt, order

    # Put the not connectable gates in the front
    connections.remove(error_gates)
    connections.insert(0, error_gates)
    attempt += 1

    return connections, attempt, order


def alter_connection_order(connections, order, chip):
    """
    Drastically alter the order in which the connections are presented to the
    algorithm.

    Args:
        connections (list): The way the gates will be connected
        order (int): Which order of the connections needs to be readied
        chip (object): Internal representation of the chip

    Returns:
       connections (list): The way the gates will be connected
    """
    # Sort the connections by distance between gates from shortest to longest
    if order >= 2:
        length_order = {}

        for connect in connections:
            reorder = connect.strip("\n").split(",")
            source_coords = [chip.gates[reorder[0]]["x"], chip.gates[reorder[0]]["y"], 0]
            target_coords = [chip.gates[reorder[1]]["x"], chip.gates[reorder[1]]["y"], 0]
            gate_dif = abs(source_coords[0] - target_coords[0]) + abs(source_coords[1] - target_coords[1])

            # Check if there are gates with the same distance
            while gate_dif in length_order:
                gate_dif += .1

            length_order[gate_dif] = connect

        sort = sorted(length_order)
        connections = [length_order[key] for key in sort]

    # Reverse the connections order
    if order == 1 or order == 3:
        connections = connections[::-1]

    return connections


def load_coordinates(chip):
    """
Initiate all the coordinate classes in each layer and add their possible connections

    Args:
        chip (object): Internal representation of the chip

    Returns:
        chip (object): Updated internal representation of the chip
    """
    for z in range(8):
        # Initiate a pre-filled grid
        chip.coordinates.append([[0 for x in range(chip.width)] for y in range(chip.height)])

        # Iterate through the grid
        for y in range(chip.height):
            for x in range(chip.width):
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

    return chip


def load_gates(chip):
    """
    Initiate Gate classes and add them to the internal representation of the grid.
    """
    for gate_id in chip.gates:
        gate_coord = chip.gates[gate_id]
        gate = gt.Gate(gate_id, gate_coord["x"], gate_coord["y"])
        chip.coordinates[0][gate_coord["y"]][gate_coord["x"]].gate = gate

    return chip


def save_csv(net, wires, net_id, chip_id, chip):
    """
    Save the cheapest cost grid as a csv file.

    Args:
        net (list): The connected gates
        wires (list): The paths of which a connection consists
        net_id ([type]): ID to identify the current netlist
        chip_id (int): ID to identify the current chip
        chip (object): Internal representation of the chip
    """
    with open('output/output.csv', 'w') as file:
        # Write first line
        output = csv.writer(file)
        output.writerow(["net", "wires"])

        # Index and fill the body
        for step in range(len(wires)):
            output.writerow([net[step],wires[step]])

        # End of file
        output.writerow([f"chip_{chip_id}_net_{net_id}", chip.cost])


def prepare_gates(chip, source_gate, target_gate):
    """
    Prepare the gates nd chip to be run throught the algorithm.

    Args:
        chip (object): Internal representation of the chip
        source_gate (int): The gate from which the algorithm will start
        target_gate (int): The gate which the algorithm will try to reach

    Returns (same variables as run_algorithm()):
        final_path (list of int): The coordinates of the path from start to goal
        cheapest_path_cost (int): The total cost of the cheapest path
        chip (object): Internal representation of the chip
    """
    crossroad = []
    travelled_path = []

    # Source and target always on z-axis 0
    source_coords = [chip.gates[source_gate]["x"], chip.gates[source_gate]["y"], 0]
    target_coords = [chip.gates[target_gate]["x"], chip.gates[target_gate]["y"], 0]

    chip = calculate_distance(target_coords, chip)

    start = chip.coordinates[0][source_coords[1]][source_coords[0]]
    start_node = nd.Node(source_coords, None, 1, start.cost + start.distance_to_goal)
    goal_node = nd.Node(target_coords, None, 1, 0)
    crossroad.append(start_node)

    return run_algorithm(target_coords, start_node, goal_node, chip, crossroad, travelled_path)


def run_algorithm(target_coords, start_node, goal_node, chip, crossroad, travelled_path):
    """
    Run the algorithm.

    Args:
        source_coords (int): The gate coordinates from which the algorithm will start
        target_coords (int): The gate coordinates which the algorithm will try to reach
        start_node ([type]): The heuristics from the start coordinates
        goal_node ([type]): The heuristics from the goal coordinates

    Returns:
        final_path (list of int): The coordinates of the path from start to goal
        cheapest_path_cost (int): The total cost of the cheapest path
        chip (object): Internal representation of the chip
    """
    cheapest_path = []
    cheapest_path_cost = 0
    retrace = False
    path_count = 0
    latest_addition = start_node

    while len(crossroad) > 0:
        # Make no more than 5 attempts at reaching the goal node
        if path_count > 5:
            break

        crossroad.sort()

        # Retrieve the node with the lowest cost
        current_node = crossroad.pop(0)

        # Retrace steps to look if a cheaper path exists
        if retrace:
            retrace = False

            while current_node.parent != travelled_path[-1]:
                del travelled_path[-1]

                if not travelled_path:
                    break

        travelled_path.append(current_node)

        # Check whether the the goal has been reached
        if current_node == goal_node:
            path_count += 1
            path, cost, retrace = retrace_path(current_node, start_node, chip)

            # Save the cheapest path
            if cost < cheapest_path_cost or cheapest_path_cost == 0:
                cheapest_path = copy.deepcopy(path)
                cheapest_path_cost = cost

        (x, y, z) = current_node.position

        neighbours = [(x-1, y, z), (x, y-1, z), (x, y+1, z), (x+1, y, z), (x, y, z+1), (x, y, z-1)]
        chip = calculate_distance(target_coords, chip)

        if crossroad:
            latest_addition = crossroad[-1]

        # Try to find the cheapest node without collisions
        for next_door in neighbours:
            crossroad = check_directions(next_door, current_node, goal_node, chip, crossroad, travelled_path, False)

        if crossroad:
            # Check whether a new node has been added
            if current_node != start_node and latest_addition == crossroad[-1]:

                # Try to find the cheapest node with collisions
                for next_door in neighbours:
                    crossroad = check_directions(next_door, current_node, goal_node, chip, crossroad, travelled_path, True)

    final_path, chip = revalue_coordinates(cheapest_path, start_node, chip, goal_node)

    return final_path, cheapest_path_cost, chip


def revalue_coordinates(cheapest_path, start_node, chip, goal_node):
    """
    Args:
        start_node (object): The heuristics from the start coordinates
        chip (object): Internal representation of the chip
        goal_node (object): The heuristics from the goal coordinates
        cheapest_path (list of int): The nodes of the path from start to goal

    Returns:
        final_path (list of int): The coordinates of the path from start to goal
        chip (object): Internal representation of the chip
    """
    final_path = []

    # Revalue the coordinates of the cheapest path
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
            chip.coordinates[z][y][x].used = True
            chip.coordinates[z][y][x].cost = 301

    return final_path, chip


def retrace_path(current_node, start_node, chip):
    """
    Retrieve the taken path from one gate to another, from goal to start.

    Args:
        current_node (object): The heuristics form the current coordinates
        start_node (object): The heuristics from the start coordinates
        chip (object): Internal representation of the chip

    Returns:
        path (list of int): Coordinates of the taken path from start to goal
        path_cost (int): Cost of the current path
        (bool): Inidicates that the search for a newer path can begin
    """
    path = []
    path_cost = 0
    collisions = 0

    while current_node != start_node:
        # Add the cost for the wires
        path_cost += 1
        x = current_node.position[0]
        y = current_node.position[1]
        z = current_node.position[2]

        # Keep track of collisions
        if chip.coordinates[z][y][x].used:
            collisions =+ 1

        path.append(current_node)
        current_node = current_node.parent

    # Add the costs for the collisions
    path_cost += collisions * 300

    # Add the start node
    path.append(current_node)

    # Reverse the order of the path
    return path[::-1], path_cost, True


def check_directions(next_door, current_node, goal_node, chip, crossroad, travelled_path, colide):
    """
    Check a neighbouring coordinate on validity.

    Args:
        next_door (int): Coordinates of a crossing next to the current coordinate
        current_node (object): The heuristics form the current coordinates
        goal_node (object): The heuristics from the goal coordinates
        target_coords (int): The gate coordinates which the algorithm will try to reach

    Returns:
        crossroad (list of objects): All the possible paths the algorithm can choose
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

    neighbour = nd.Node(next_door, current_node, next_node.cost, next_node.cost + next_node.distance_to_goal)

    if neighbour != goal_node and chip.coordinates[next_door[2]][next_door[1]][next_door[0]].gate is not None:
        return crossroad

    # Check whether the coordinate is already in the current path.
    if neighbour in travelled_path:
        return crossroad

    # Check whether neighbor is in open list and if it has a lower cost value
    if add_to_crossroad(neighbour, crossroad, colide):
        crossroad.append(neighbour)

    return crossroad


def calculate_distance(target_coords, chip):
    """
    Calculate the distance to the goal from all the coordinates.

    Args:
        target_coords (int): The gate coordinates which the algorithm will try to reach
        chip (object): Internal representation of the chip

    Returns:
        chip (object): Internal representation of the chip
    """

    for z in chip.coordinates:
        for y in z:
            for x in y:
                x.distance_to_goal = abs(x.x_coord - target_coords[0])
                x.distance_to_goal += abs(x.y_coord - target_coords[1])
                x.distance_to_goal += abs(x.z_coord - target_coords[2])

    return chip


def add_to_crossroad(neighbour, crossroad, colide):
    """ 
    Check to see of the coordinate is cheap enough.

    Args:
        neighbour (object): Heuristics of coordiantes next to the current coordinate
        crossroad (list of objects): All the possible paths the algorithm can choose
        goal_node (object): The heuristics from the goal coordinates

    Returns:
        bool: Whether to add or not to add to crossroad
    """
    # Allow collisions of wires
    if colide:
        for node in crossroad:
            if neighbour.heuristic - 300 > node.heuristic or neighbour.heuristic < 300:
                return False

    # Do not allow collisions of wires
    else:
        for node in crossroad:
            if neighbour.heuristic > node.heuristic:
                return False

    return True
