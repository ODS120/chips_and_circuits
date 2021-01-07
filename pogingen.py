# Poging 1:
# Deze oplossing is niet tot werking gekomen doordat de connecties nu niet meer volledig gemaakt mogen worden.
# Zoals te zien in de resultaten hieronder, kan in dit geval specifiek gate 4 niet aan gate 2 worden verbonden 
# omdat deze al een connectie heeft naar "west" met gate 1, en dus niet voldoet aan de voorwaarde van het niet
# hebben van verbindingen.
# 1
# EAST
# EAST
# EAST
# EAST
# EAST
# 1
# SOUTH
# EAST
# EAST
# EAST
# 3
# SOUTH
# WEST
# SOUTH
# SOUTH
# 4
# NORTH
# NORTH
''''
    # north
    if draw_y < gate_b["y_coord"] and not self.coordinates[draw_x][draw_y + 1].connections:
        draw_y = self.wire_north(draw_x, draw_y)
    # east
    elif draw_x < gate_b["x_coord"] and not self.coordinates[draw_x + 1][draw_y].connections:
        draw_x = self.wire_east(draw_x, draw_y)
    # west
    elif draw_x > gate_b["x_coord"] and not self.coordinates[draw_x - 1][draw_y].connections:
        draw_x = self.wire_west(draw_x, draw_y)
    # south
    elif draw_y > gate_b["y_coord"] and not self.coordinates[draw_x][draw_y - 1].connections:
        draw_y = self.wire_south(draw_x, draw_y)
'''

