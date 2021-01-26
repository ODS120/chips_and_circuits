
class Coordinate(): 
    """
    Run path search algorithm

    Args:
        chip ([type]): [description]
        source_node ([type]): [description]
        goal_node ([type]): [description]
        wire_id ([type]): [description]
    
    Returns:
        [Bool]: [description]
    """   
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
        self.wire_ids = []

    # compare nodes
    def __eq__(self, other):
        return self.x_coord == other.x_coord and self.y_coord == other.y_coord and self.z_coord == other.z_coord

    # print node
    def __repr__(self):
        return ('({0},{1},{2})'.format(self.x_coord, self.y_coord, self.z_coord))