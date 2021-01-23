    def wire(self, draw_x, draw_y, colour, direction):
        # add direction to current coordinate
        self.coordinates[draw_x][draw_y].connections.append(direction)

        if direction == "north" or direction == "south":
            # hold the x-coordinates of the line
            x1 = [draw_x, draw_x]

            # calculate a line to the north
            if direction == "north":
                self.coordinates[draw_x][draw_y + 1].connections.append("south")
                y1 = [draw_y, draw_y + 1]
                draw_y += 1
            # calculate a line to the south
            else:
                self.coordinates[draw_x][draw_y - 1].connections.append("north")
                y1 = [draw_y, draw_y - 1]
                draw_y -= 1
        
        elif direction == "east" or direction == "west":
            # hold the y-coordinates of the line
            y1 = [draw_y, draw_y]

            # calculate a line to the east
            if direction == "east":
                self.coordinates[draw_x + 1][draw_y].connections.append("west")
                x1 = [draw_x + 1, draw_x]
                draw_x += 1
            # calculate a line to the west
            else:
                self.coordinates[draw_x - 1][draw_y].connections.append("east")
                x1 = [draw_x - 1, draw_x]
                draw_x -= 1

        # draw the line        
        plt.plot(x1, y1, colour)
        print(colour)

        # return current position on the grid
        return draw_x, draw_y