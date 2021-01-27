"""
gate.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Implements the internal representation of a gate.
"""

class Gate():
    def __init__(self, gate_id, x, y):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y