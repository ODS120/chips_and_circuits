class Gate():
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
    def __init__(self, gate_id, x, y, z, node):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.node = node