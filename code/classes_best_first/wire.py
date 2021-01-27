"""
wire.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Implements the internal representation of a chip.
"""

class Wire():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.used = False
        self.total_cost = 0
