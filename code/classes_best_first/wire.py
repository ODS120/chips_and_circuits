class Wire():
    # stores wire found by algorithm 
    def __init__(self, x, y, z):
        # self.wire_id = wire_id
        self.x = x
        self.y = y
        self.z = z
        self.used = False
        self.total_cost = 0

    def add_wire(self, to_node, cost):
        pass
        # stores node objects
        # self.nodes.append(to_node)
        # self.total_cost += cost