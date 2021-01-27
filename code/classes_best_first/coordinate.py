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
        self.gate = None
        self.connections = {}
        self.used = False
        self.cost = 1
        self.distance_to_goal = 0 