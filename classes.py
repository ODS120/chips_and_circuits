class Chip():
    def __init__(self, filename):
        self.height = 0
        self.width = 0
        self.coordinates = []

        self.load_grid(filename)
        self.load_coordinates()
        self.load_gates(filename)

    # load the grid
    def load_grid(self, filename):
        with open(filename) as chip_grid:
            next(chip_grid)

            # find the max x and y coordinate
            for line in chip_grid:
                coordinates = line.split(",")

                if coordinates[1] > self.width:
                    self.width = coordinates[1]

                if coordinates[2] > self.height:
                    self.height = coordinates[2]
            
            # add borders to the grid
            self.width += 2
            self.height += 2


    # load all the coordinate classes
    def load_coordinates(self):
        # iterate over all the grid coordinates
        for y_coord in self.height:
            self.coordinates[y_coord] = []

            for x_coord in self.width:
                coordinate = Coordinate(x_coord, y_coord)
                self.coordinates[y_coord][x_coord] = coordinate


    # load all the gate classes
    def load_gates(self, filename):
        with open(filename) as chip_grid:
            next(chip_grid)

            for line in chip_grid:
                gate_info = line.split(",")
                gate_object = Gate(gate_info[0], gate_info[1], gate_info[2])
                # appoint the gate its position on the grid
                self.coordinates[gate_info[1]][gate_info[2]].gate = gate_object


class Coordinate(): 
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.gate = []
        # north, east, south, west, up, down
        self.connections = []   


class Gate():
    def __init__(self, gate_id, x, y):
        self.gate_id = gate_id
        self.x_coord = x
        self.y_coord = y
