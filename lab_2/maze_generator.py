import random


class MazeGenerator:

    def __init__(self, width, height):  # width and height with borders around | w = 23, h = 13
        self.width = width
        self.height = height
        self.walls = []
        self.unvisited_points = (width-1)/2 * (height-1)/2
        # self.unvisited_points = 66
        self.dead_end = []
        self.dir = 1

    def generate_maze(self):
        self.walls = [[True for j in range(self.width)] for i in range(self.height)]
        self.walls[1][1] = False
        self.dead_end.append([1,1])

        self.recursion_for_maze_gen([1, 1])
        self.remove_dead_ends()
        self.add_ghost_home()

        return self.walls

    def add_ghost_home(self):
        x = [5, 6, 7, 8, 9]
        y = [7, 8, 9, 10, 11, 12, 13, 14, 15]

        for i in x:
            self.walls[i][8] = True
            self.walls[i][14] = True
        for j in y:
            self.walls[6][j] = True
            self.walls[8][j] = True

        for i in x:
            self.walls[i][7] = False
            self.walls[i][15] = False
        for j in y:
            self.walls[5][j] = False
            self.walls[9][j] = False

        self.walls[6][10] = False
        self.walls[6][11] = False
        self.walls[6][12] = False

        self.walls[7][9] = False
        self.walls[7][10] = False
        self.walls[7][11] = False
        self.walls[7][12] = False
        self.walls[7][13] = False



    def recursion_for_maze_gen(self, current_xy):
        self.unvisited_points -= 1

        while self.unvisited_points != 0:
            directions = self.get_move_direction(current_xy)
            if len(directions) != 0:
                new_xy = random.choice(directions)
                move_to = self.interpret_direction_to_string(current_xy, new_xy)
                self.change_walls(current_xy, move_to)
                self.dir = 1
                self.recursion_for_maze_gen(new_xy)
            else:
                if self.dir == 1:
                    self.dead_end.append(current_xy)
                self.dir = -1
                break

    def remove_dead_ends(self):
        for end in self.dead_end:
            directions = self.get_dead_end_direction(end)
            if len(directions) != 0:
                new_xy = random.choice(directions)
                if new_xy in self.dead_end:
                    self.dead_end.pop(self.dead_end.index(new_xy))
                move_to = self.interpret_direction_to_string(end, new_xy)
                self.change_walls(end, move_to)

    def get_move_direction(self, current_xy):
        directions = []

        x_p2 = current_xy[0] + 2
        x_m2 = current_xy[0] - 2
        y_p2 = current_xy[1] + 2
        y_m2 = current_xy[1] - 2

        if x_m2 != -1 and self.walls[current_xy[0] - 2][current_xy[1]] is True:
            directions.append([current_xy[0] - 2, current_xy[1]])
        if y_m2 != -1 and self.walls[current_xy[0]][current_xy[1] - 2] is True:
            directions.append([current_xy[0], current_xy[1] - 2])
        if x_p2 < self.height and self.walls[current_xy[0] + 2][current_xy[1]] is True:
            directions.append([current_xy[0] + 2, current_xy[1]])
        if y_p2 < self.width and self.walls[current_xy[0]][current_xy[1] + 2] is True:
            directions.append([current_xy[0], current_xy[1] + 2])

        return directions

    def interpret_direction_to_string(self, current_xy, new_xy):
        if new_xy[0] - current_xy[0] > 0:
            return "down"
        if new_xy[0] - current_xy[0] < 0:
            return "up"
        if new_xy[1] - current_xy[1] > 0:
            return "right"
        return "left"

    def change_walls(self, current_xy, move_to):
        if move_to == "down":
            self.walls[current_xy[0] + 1][current_xy[1]] = False
            self.walls[current_xy[0] + 2][current_xy[1]] = False
        if move_to == "up":
            self.walls[current_xy[0] - 1][current_xy[1]] = False
            self.walls[current_xy[0] - 2][current_xy[1]] = False
        if move_to == "right":
            self.walls[current_xy[0]][current_xy[1] + 1] = False
            self.walls[current_xy[0]][current_xy[1] + 2] = False
        if move_to == "left":
            self.walls[current_xy[0]][current_xy[1] - 1] = False
            self.walls[current_xy[0]][current_xy[1] - 2] = False


    def get_dead_end_direction(self, current_xy):
        directions = []

        x_p2 = current_xy[0] + 2
        x_m2 = current_xy[0] - 2
        y_p2 = current_xy[1] + 2
        y_m2 = current_xy[1] - 2

        if x_m2 != -1 and self.walls[current_xy[0] - 1][current_xy[1]] is True:
            directions.append([current_xy[0] - 2, current_xy[1]])
        if y_m2 != -1 and self.walls[current_xy[0]][current_xy[1] - 1] is True:
            directions.append([current_xy[0], current_xy[1] - 2])
        if x_p2 < self.height and self.walls[current_xy[0] + 1][current_xy[1]] is True:
            directions.append([current_xy[0] + 2, current_xy[1]])
        if y_p2 < self.width and self.walls[current_xy[0]][current_xy[1] + 1] is True:
            directions.append([current_xy[0], current_xy[1] + 2])

        return directions