"""
node.py

Chips & Circuits 2021
Martijn van Veen, Olaf Stringer, Jan-Joost Raedts

Implements the internal representation of a node.
"""

class Node():
    def __init__(self, position, parent, cost, heuristic):
        self.position = position[0], position[1], position[2]
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
    
    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
         return self.heuristic < other.heuristic

        # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.heuristic))