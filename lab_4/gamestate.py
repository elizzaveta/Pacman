import copy

class GameState:
    def __init__(self, food_amount, grid):
        self.pacman_xy = []
        self.ghosts_xy = []
        self.ghosts_types = []
        self.food_amount = food_amount
        self.score = 0
        self.food = []
        self.grid = grid

    """ update state according to game """
    def update_self(self, game):
        self.pacman_xy = [game.pacman.x, game.pacman.y]
        self.ghosts_xy = []
        for ghost in game.ghosts:
            self.ghosts_xy.append([ghost.x, ghost.y])
            self.ghosts_types.append(ghost.type)
        self.score = game.score
        self.food = copy.deepcopy(game.grid.food)

    """ imitate move while building a minimax tree """

    def imitate_move(self, player, direction):
        x_or_y = self.grid.dir_x_or_y(direction)
        move_delta = self.grid.dir_index(direction)
        if_was_food = False

        if player == 0:
            if x_or_y == "x":
                self.pacman_xy[0] = self.pacman_xy[0] + move_delta
            else:
                self.pacman_xy[1] = self.pacman_xy[1] + move_delta
            if self.food[self.pacman_xy[0]][self.pacman_xy[1]] == '1':
                self.score += 1
                self.food[self.pacman_xy[0]][self.pacman_xy[1]] = '0'
                if_was_food = True

        else:
            if x_or_y == "x":
                self.ghosts_xy[player - 1][0] = self.ghosts_xy[player - 1][0] + move_delta
            else:
                self.ghosts_xy[player - 1][1] = self.ghosts_xy[player - 1][1] + move_delta

        return if_was_food

    """ undo move while building a minimax tree """
    def undo_move(self, player, direction, if_was_food=False):
        x_or_y = self.grid.dir_x_or_y(direction)
        move_delta = self.grid.dir_index(direction)

        if player == 0:
            if x_or_y == "x":
                self.pacman_xy[0] = self.pacman_xy[0] - move_delta
            else:
                self.pacman_xy[1] = self.pacman_xy[1] - move_delta

            if if_was_food:
                self.score -= 1
                self.food[self.pacman_xy[0]][self.pacman_xy[1]] = '1'
        else:
            if x_or_y == "x":
                self.ghosts_xy[player - 1][0] = self.ghosts_xy[player - 1][0] - move_delta
            else:
                self.ghosts_xy[player - 1][1] = self.ghosts_xy[player - 1][1] - move_delta

