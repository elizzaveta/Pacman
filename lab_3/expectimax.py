from minimax import *

class Expectimax:
    def __init__(self, food_amount, grid, probability):
        self.min = -1000
        self.max = 1000
        self.game_state = GameState(food_amount, grid)
        self.prev_pacman_xy = []
        self.best_pacman_xy = []
        self.best_pacman_dir = ""
        self.max_depth = 9
        self.probability = probability

    def run(self, prev_state_xy, game):
        self.game_state.update_self(game)
        self.prev_pacman_xy = prev_state_xy
        a = [self.game_state.pacman_xy[0], self.game_state.pacman_xy[1]]
        self.expectimax(0, 0)
        return self.best_pacman_dir

    def expectimax(self,depth, player_index):
        if self.game_state.pacman_xy in self.game_state.ghosts_xy:
            return self.game_state.score - self.game_state.food_amount
        if depth == self.max_depth or  self.game_state.score == self.game_state.food_amount:
            return self.estimate_state_value(player_index)

        if player_index > len(self.game_state.ghosts_xy): player_index = 0


        if player_index == 0:
            best = self.min
            # print("---depth: ", depth)
            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.pacman_xy[0],
                                                                               self.game_state.pacman_xy[1])
            for i in directions:

                if_was_food = self.imitate_move(0, i)
                val = self.expectimax(depth + 1, player_index + 1)
                if self.game_state.pacman_xy == self.prev_pacman_xy:
                    val -= 1
                self.undo_move(0, i, if_was_food)

                if depth == 0:
                    a = 0
                    print("val from", self.prev_pacman_xy, " to ", i, " is = ", val)

                if val > best and depth == 0:
                    self.best_pacman_dir = i
                best = max(best, val)


            return best
        elif self.game_state.ghosts_types[player_index-1] == "random":
            sum = 0

            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.ghosts_xy[player_index-1][0],
                                                                               self.game_state.ghosts_xy[player_index-1][1])
            for i in directions:

                self.imitate_move(player_index, i)
                val = self.expectimax(depth + 1, player_index + 1)
                self.undo_move(player_index, i)

                sum += val

            return sum/len(directions)
        else:
            sum = 0
            best = self.max
            best_move_val = 0

            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.ghosts_xy[player_index-1][0],
                                                                               self.game_state.ghosts_xy[player_index-1][1])

            dir_n = len(directions)
            if dir_n!=1:
                random_prob = (1-self.probability)/(dir_n-1)
            else:
                random_prob = 0

            for i in directions:
                self.imitate_move(player_index, i)
                val = self.expectimax(depth + 1, player_index + 1)
                self.undo_move(player_index, i)

                sum += val
                if val<best:
                    best_move_val = val
                best = min(best, val)

            return (sum-best_move_val) * random_prob + best_move_val*self.probability



    def estimate_state_value(self, player_ind):
        return self.game_state.score








    def if_ghost_near(self):
        for ghost in self.game_state.ghosts_xy:
            if abs(self.game_state.pacman_xy[0] - ghost[0]) == 1 or abs(
                    self.game_state.pacman_xy[1] - ghost[1]) == 1:
                return -1
        return 0

    def imitate_move(self, player, direction):
        x_or_y = self.game_state.grid.dir_x_or_y(direction)
        move_delta = self.game_state.grid.dir_index(direction)
        if_was_food = False

        if player == 0:
            if x_or_y == "x":
                self.game_state.pacman_xy[0] = self.game_state.pacman_xy[0] + move_delta
            else:
                self.game_state.pacman_xy[1] = self.game_state.pacman_xy[1] + move_delta
            if self.game_state.food[self.game_state.pacman_xy[0]][self.game_state.pacman_xy[1]] == '1':
                self.game_state.score += 1
                self.game_state.food[self.game_state.pacman_xy[0]][self.game_state.pacman_xy[1]] = '0'
                if_was_food = True

        else:
            if x_or_y == "x":
                self.game_state.ghosts_xy[player-1][0] = self.game_state.ghosts_xy[player-1][0] + move_delta
            else:
                self.game_state.ghosts_xy[player-1][1] = self.game_state.ghosts_xy[player-1][1] + move_delta

        return if_was_food


    def undo_move(self, player, direction, if_was_food = False):
        x_or_y = self.game_state.grid.dir_x_or_y(direction)
        move_delta = self.game_state.grid.dir_index(direction)

        if player == 0:
            if x_or_y == "x":
                self.game_state.pacman_xy[0] = self.game_state.pacman_xy[0] - move_delta
            else:
                self.game_state.pacman_xy[1] = self.game_state.pacman_xy[1] - move_delta

            if if_was_food:
                self.game_state.score -= 1
                self.game_state.food[self.game_state.pacman_xy[0]][self.game_state.pacman_xy[1]] = '1'
        else:
            if x_or_y == "x":
                self.game_state.ghosts_xy[player - 1][0] = self.game_state.ghosts_xy[player - 1][0] - move_delta
            else:
                self.game_state.ghosts_xy[player - 1][1] = self.game_state.ghosts_xy[player - 1][1] - move_delta

    def dist(self, ghost_ind):

        return abs(self.game_state.pacman_xy[0] - self.game_state.ghosts_xy[ghost_ind-1][0]) + abs(self.game_state.pacman_xy[1] - self.game_state.ghosts_xy[ghost_ind-1][1])









