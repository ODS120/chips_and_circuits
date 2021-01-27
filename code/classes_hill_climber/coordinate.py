"""
coordinate.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Implements the internal representation of a coordinate.
"""


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
        self.heuristic = None

        self.parent = None
        self.path_ids = []

    # Compare nodes
    def __eq__(self, other):
        return self.x_coord == other.x_coord and self.y_coord == other.y_coord and self.z_coord == other.z_coord

    # Print node
    def __repr__(self):
        return ('({0},{1},{2})'.format(self.x_coord, self.y_coord, self.z_coord))