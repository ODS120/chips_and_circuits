class Coordinate(): 
    def __init__(self, x, y, z):
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.gate = None
        # north, east, south, west, up, down
        self.connections = {}
        self.used = False
        self.cost = 1
        self.distance_to_goal = 0 