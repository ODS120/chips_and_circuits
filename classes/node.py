class Node():
    def __init__(self, position, parent, cost):
        self.position = [position[0], position[1], position[2]]
        self.parent = parent
        self.cost = cost
    
    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
         return self.cost < other.cost

        # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.cost))