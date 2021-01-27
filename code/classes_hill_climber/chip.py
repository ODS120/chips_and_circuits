"""
chip.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Implements the internal representation of a chip.
"""

import csv
from . import coordinate as crd
from . import gate as gt


class Chip():
    def __init__(self, chip_data):
        self.height = 0
        self.width = 0
        self.depth = 7
        self.coordinates = []
        self.gates = {}
        self.path_data = {}

        self.best_cost = float("inf")
        self.best_length = 0
        self.best_paths_data = []

        # prepare the chip to be worked with
        self.load_grid(chip_data)
        self.load_coordinates()
        self.load_gates()

    def load_grid(self, chip_data):
        """
        Create an internal 3d grid on which the case will be represented

        Args:
            chip_data (file): The coordinates of the gates
        """   
        with open(chip_data) as chip_grid:
            next(chip_grid)
            # Iterate over chip data; store gate info and largest coordinates of the chip
            for line in chip_grid:
                gate_info = line.strip("\n").split(",")
                self.gates[gate_info[0]] = {"x_coord": int(gate_info[1]), "y_coord": int(gate_info[2]), "z_coord": 0, "node_object": None,  }

                # Find the max x and y coordinate
                if int(gate_info[1]) > self.width:
                    self.width = int(gate_info[1])
                if int(gate_info[2]) > self.height:
                    self.height = int(gate_info[2])

            # Add borders to the grid
            self.width += 2
            self.height += 2 


    # Load all the coordinate classes
    def load_coordinates(self):
        """
        Create 3d list with coordinate node objects

        """   
        # Create 3d grid list with node objects
        self.coordinates = [[[crd.Coordinate(x, y, z) for z in range(8)] for y in range(self.height)] for x in range(self.width)]

        # Find neighbours for every coordinate node
        for x in range(self.width):
            for y in range(self.height):
                for z in range(8):
                    coordinate = self.coordinates[x][y][z]

                    # Get x axis neighbours
                    if x + 1 < self.width:
                        coordinate.neighbours.append(self.coordinates[x+1][y][z])
                    if x - 1 >= 0:
                        coordinate.neighbours.append(self.coordinates[x-1][y][z])
                    # Get y axis neighbours
                    if y + 1 < self.height:
                        coordinate.neighbours.append(self.coordinates[x][y+1][z])
                    if y - 1 >= 0:
                        coordinate.neighbours.append(self.coordinates[x][y-1][z])
                    # Get z axis neighbours
                    if z + 1 < 8:
                        coordinate.neighbours.append(self.coordinates[x][y][z+1])
                    if z - 1 >= 0:
                        coordinate.neighbours.append(self.coordinates[x][y][z-1])


    def load_gates(self):
        """
        Create all gate objects

        """   
        # Iterate over all gates
        for gate_id in self.gates:
            gate_info = self.gates[gate_id]
            # Create gate object
            gate_object = gt.Gate(gate_id, gate_info["x_coord"], gate_info["y_coord"], gate_info["z_coord"], self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]])
            
            self.gates[gate_id]["node_object"] = self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]]
            self.coordinates[gate_info["x_coord"]][gate_info["y_coord"]][gate_info["z_coord"]].gate = gate_object

            # Add extra bonus cost for the neighbouring nodes of a gate node
            for gate_neighbour in gate_object.node.neighbours:
                gate_neighbour.near_gate_cost = .5