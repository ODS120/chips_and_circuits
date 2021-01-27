"""
classes.py
"""
import csv
import random
import os
import matplotlib.pyplot as plt

import coordinate as crd
import wire as wr

class Chip():
    def __init__(self, chip_data, netlist):
        self.height = 0
        self.width = 0
        self.depth = 7
        self.coordinates = []
        self.gates = {}
        self.cost = 0
        self.collisions = 0

        # Filter id names
        self.chip_id = os.path.basename(chip_data).replace("print_", "").replace(".csv",  "")
        self.net_id = os.path.basename(netlist).replace("netlist_", "").replace(".csv", "")

        # Prepare the chip to be worked with
        self.load_grid(chip_data)


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
                self.gates[gate_info[0]] = {"x": int(gate_info[1]), "y": int(gate_info[2])}

                # Find the max x and y coordinate
                if int(gate_info[1]) > self.width:
                    self.width += int(gate_info[1])

                if int(gate_info[2]) > self.height:
                    self.height += int(gate_info[2])
            
            # Add borders to the grid
            self.width += 2
            self.height += 2 
