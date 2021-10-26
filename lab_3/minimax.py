from gamestate import *

class Minimax:

    def __init__(self, food_amount, grid, alg, probability=None):
        self.min = -1000
        self.max = 1000
        self.game_state = GameState(food_amount, grid)
        self.prev_pacman_xy = []
        self.best_pacman_xy = []
        self.best_pacman_dir = ""
        self.max_depth = 9
        self.algorithm = alg
        self.probability = probability

    """ run minimax """
    def run(self, prev_state_xy, game):
        self.game_state.update_self(game)
        self.prev_pacman_xy = prev_state_xy
        if self.algorithm == "alpha-beta":
            self.minimax_ab(0, 0, self.min, self.max)
        elif self.algorithm == "expectimax":
            self.expectimax(0, 0)
        return self.best_pacman_dir

    """ Alpha-Beta Pruning algorithm """
    def minimax_ab(self, depth, player_index, alpha, beta):

        if self.game_state.pacman_xy in self.game_state.ghosts_xy:
            return self.game_state.score - self.game_state.food_amount
        if depth == self.max_depth or  self.game_state.score == self.game_state.food_amount:
            return self.estimate_state_value()

        if player_index > len(self.game_state.ghosts_xy): player_index = 0


        if player_index == 0:
            best = self.min
            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.pacman_xy[0], self.game_state.pacman_xy[1])
            for i in directions:
                if_was_food = self.game_state.imitate_move(0,i)
                val = self.minimax_ab(depth+1, player_index+1, alpha, beta)
                if self.game_state.pacman_xy == self.prev_pacman_xy:
                    val-=1
                self.game_state.undo_move(0, i, if_was_food)

                if val>best and depth == 0:
                    self.best_pacman_dir = i
                best = max(best, val)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best
        else:
            best = self.max

            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.ghosts_xy[player_index-1][0], self.game_state.ghosts_xy[player_index-1][1])
            for i in directions:  # to do: проход по всем узлам, вариантам хода

                self.game_state.imitate_move(player_index, i)
                val = self.minimax_ab(depth +1, player_index+1,  alpha, beta)
                self.game_state.undo_move(player_index, i)

                best = min(best, val)
                beta = min(beta, best)

                if beta <= alpha:
                    break
            return best

    """ Expectimax algorithm """
    def expectimax(self,depth, player_index):
        if self.game_state.pacman_xy in self.game_state.ghosts_xy:
            return self.game_state.score - self.game_state.food_amount
        if depth == self.max_depth or  self.game_state.score == self.game_state.food_amount:
            return self.estimate_state_value()

        if player_index > len(self.game_state.ghosts_xy): player_index = 0

        if player_index == 0:
            best = self.min
            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.pacman_xy[0],
                                                                               self.game_state.pacman_xy[1])
            for i in directions:

                if_was_food = self.game_state.imitate_move(0, i)
                val = self.expectimax(depth + 1, player_index + 1)
                if self.game_state.pacman_xy == self.prev_pacman_xy:
                    val -= 1
                self.game_state.undo_move(0, i, if_was_food)

                if val > best and depth == 0:
                    self.best_pacman_dir = i
                best = max(best, val)
            return best
        elif self.game_state.ghosts_types[player_index-1] == "random":
            sum = 0

            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.ghosts_xy[player_index-1][0],
                                                                               self.game_state.ghosts_xy[player_index-1][1])
            for i in directions:

                self.game_state.imitate_move(player_index, i)
                val = self.expectimax(depth + 1, player_index + 1)
                self.game_state.undo_move(player_index, i)

                sum += val

            return sum/len(directions)
        else:
            sum = 0
            best = self.max
            best_move_val = 0

            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.ghosts_xy[player_index-1][0],
                                                                               self.game_state.ghosts_xy[player_index-1][1])

            dir_n = len(directions)
            if dir_n != 1:
                random_prob = (1-self.probability)/(dir_n-1)
            else:
                random_prob = 0

            for i in directions:
                self.game_state.imitate_move(player_index, i)
                val = self.expectimax(depth + 1, player_index + 1)
                self.game_state.undo_move(player_index, i)

                sum += val
                if val<best:
                    best_move_val = val
                best = min(best, val)

            return (sum-best_move_val) * random_prob + best_move_val*self.probability

    """ estimated value of current game state """
    def estimate_state_value(self):
        return self.game_state.score + self.if_ghost_near()

    """ decrease value of state if ghost is near pacman """
    def if_ghost_near(self):
        for ghost in self.game_state.ghosts_xy:
            if abs(self.game_state.pacman_xy[0] - ghost[0]) == 1 or abs(
                    self.game_state.pacman_xy[1] - ghost[1]) == 1:
                return -1
        return 0




