import copy


class GameState:
    def __init__(self, food_amount, grid):
        self.pacman_xy = []
        self.ghosts_xy = []
        self.food_amount = food_amount
        self.score = 0
        self.food = []
        self.grid = grid

    def update_self(self, game):
        self.pacman_xy = [game.pacman.x, game.pacman.y]
        self.ghosts_xy = []
        for ghost in game.ghosts:
            self.ghosts_xy.append([ghost.x, ghost.y])
        self.score = game.score
        self.food = copy.deepcopy(game.grid.food)

class Minimax:

    def __init__(self, food_amount, grid):
        self.min = -1000
        self.max = 1000
        self.game_state = GameState(food_amount, grid)
        self.prev_pacman_xy = []
        self.best_pacman_xy = []
        self.max_depth = 15

    def run(self, game, prev_state_xy):
        self.game_state.update_self(game)
        self.prev_pacman_xy = prev_state_xy
        a = [self.game_state.pacman_xy[0], self.game_state.pacman_xy[1]]
        val = self.minimax(0, 0, self.min, self.max)
        print("prev: ", self.prev_pacman_xy," current: ",a, " new: ", self.best_pacman_xy, " val: ", val)
        return self.best_pacman_xy

    def minimax(self, depth, player_index, alpha, beta):

        if self.game_state.pacman_xy in self.game_state.ghosts_xy:
            return self.game_state.score - self.game_state.food_amount
        if self.game_state.score == self.game_state.food_amount:
            return self.game_state.score
        if depth == self.max_depth:
            return self.estimate_state_value()

        # if player_index!= 0:
        #     while self.move_to_other_ghost(player_index):
        #         player_index+=1

        if player_index > len(self.game_state.ghosts_xy): player_index = 0

        if player_index == 0:
            best = self.min
            # print("---depth: ", depth)
            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.pacman_xy[0], self.game_state.pacman_xy[1])
            for i in directions:  # to do: проход по всем узлам, вариантам хода

                if_was_food = self.imitate_move(0,i)

                val = self.minimax(depth+1, player_index+1, alpha, beta)

                if self.game_state.pacman_xy == self.prev_pacman_xy:
                    val -= 3

                # print(depth, "level, p_xy: ", self.game_state.pacman_xy, " value: ", val)

                self.undo_move(0, i, if_was_food)

                best = max(best, val)
                alpha = max(alpha, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    self.best_pacman_xy = copy.deepcopy(self.game_state.pacman_xy)
                    break
            return best
        else:
                # maybe if ghost is not important we can skip his movement in range of allowed depth <-----

            

            best = self.max

            directions = self.game_state.grid.get_possible_directions_for_move(self.game_state.pacman_xy[0], self.game_state.pacman_xy[1])
            for i in directions:  # to do: проход по всем узлам, вариантам хода

                self.imitate_move(player_index, i)
                val = self.minimax(depth +1, player_index+1,  alpha, beta)
                self.undo_move(player_index, i)

                best = min(best, val)
                beta = min(beta, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    self.best_pacman_xy = copy.deepcopy(self.game_state.pacman_xy)
                    break
            return best


    def estimate_state_value(self):
        value = self.game_state.score





        return value



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

    def move_to_other_ghost(self, ghost_ind):
        if ghost_ind > len(self.game_state.ghosts_xy):
            return False

        dist = abs(self.game_state.pacman_xy[0] - self.game_state.ghosts_xy[ghost_ind-1][0]) + abs(self.game_state.pacman_xy[1] - self.game_state.ghosts_xy[ghost_ind-1][1])
        if dist > self.max_depth/ len(self.game_state.ghosts_xy):
            return True
        return False


