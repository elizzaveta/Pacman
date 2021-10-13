"""
0 - pacman
1 - ghost
"""



class Agent:

    def __init__(self, player_ind, x, y):

        self.player = player_ind
        self.x = x
        self.y = y
        self.left = True
        self.right = False
        self.up = False
        self.down = False
        if player_ind == 2:
            self.left = False
            self.right = True

    """ change move direction """
    def change_direction(self, direction):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        if direction == "left":
            self.left = True
        elif direction == "right":
            self.right = True
        elif direction == "up":
            self.up = True
        else:
            self.down = True

    """ get current move direction"""
    def get_direction(self):
        if self.left: return "left"
        if self.right: return "right"
        if self.up: return "up"
        return "down"

    """ get direction, opposite to current """
    def get_opposite_direciton(self, dir):
        if dir == "left": return "right"
        if dir == "right": return "left"
        if dir == "up": return "down"
        if dir == "down": return "up"

    def move_to_all(self, direction, display_info, ind):
        self.change_direction(direction)
        if direction == "left":
            self.y -= 1
            display_info.agents_x[ind] -= 38
        elif direction == "right":
            self.y += 1
            display_info.agents_x[ind] += 38
        elif direction == "up":
            self.x -= 1
            display_info.agents_y[ind] -= 38
        else:
            self.x += 1
            display_info.agents_y[ind] += 38






class Ghost(Agent):

    """ make move """
    def move_to(self, direction, display_info, ind):
        self.change_direction(direction)
        if direction == "left":
            self.y -= 1
            display_info.ghost_x[ind] -= 38
        elif direction == "right":
            self.y += 1
            display_info.ghost_x[ind] += 38
        elif direction == "up":
            self.x -= 1
            display_info.ghost_y[ind] -= 38
        else:
            self.x += 1
            display_info.ghost_y[ind] += 38


class Pacman(Agent):

    """ make move """
    def move_pacman_to(self, direction, display_info):
        self.change_direction(direction)
        if direction == "left":
            self.y -= 1
            display_info.pacman_x -= 38
        elif direction == "right":
            self.y += 1
            display_info.pacman_x += 38
        elif direction == "up":
            self.x -= 1
            display_info.pacman_y -= 38
        else:
            self.x += 1
            display_info.pacman_y += 38