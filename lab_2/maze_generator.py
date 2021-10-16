import random
import copy
from grid import *
from additional_functions import *

class MazeGenerator:

    def __init__(self):  # width and height with borders around | w = 23, h = 13

        self.walls = []
        self.unvisited_points = 0
        self.dead_end = []
        self.dir = 1
        self.food = []
        self.food_amount = 0

    def get_generated_grid(self, height, width):
        self.unvisited_points = (width - 1) / 2 * (height - 1) / 2  # change to both odd and not odd
        walls = self.generate_maze(height, width)
        food = self.get_food(height, width)
        return Grid(width, height, walls, food, self.food_amount)


    def generate_maze(self, height, width):
        self.walls = [['1' for j in range(width)] for i in range(height)]
        self.walls[1][1] = '0'
        self.dead_end.append([1,1])

        self.recursion_for_maze_gen([1, 1], height, width)
        self.remove_dead_ends(height, width)
        self.add_ghost_home()

        return self.walls


    def recursion_for_maze_gen(self, current_xy, height, width):
        self.unvisited_points -= 1

        while self.unvisited_points != 0:
            directions = self.get_move_direction(current_xy, height, width)
            if len(directions) != 0:
                new_xy = random.choice(directions)
                move_to = get_direction(current_xy, new_xy)
                self.change_walls(current_xy, move_to)
                self.dir = 1
                if self.unvisited_points == 1:
                    self.dir = 2
                self.recursion_for_maze_gen(new_xy, height, width)
            else:
                if self.dir == 1:
                    self.dead_end.append(current_xy)
                self.dir = -1
                break

        if self.unvisited_points == 0 and self.dir == 2:
            self.dir = 1
            self.dead_end.append(current_xy)

    def remove_dead_ends(self, height, width):
        for end in self.dead_end:
            directions = self.get_dead_end_direction(end, height, width)
            if len(directions) != 0:
                new_xy = random.choice(directions)
                if new_xy in self.dead_end:
                    self.dead_end.pop(self.dead_end.index(new_xy))
                move_to = get_direction(end, new_xy)
                self.change_walls(end, move_to)

    def get_move_direction(self, current_xy, height, width):
        directions = []

        x_p2 = current_xy[0] + 2
        x_m2 = current_xy[0] - 2
        y_p2 = current_xy[1] + 2
        y_m2 = current_xy[1] - 2

        if x_m2 != -1 and self.walls[current_xy[0] - 2][current_xy[1]] == '1':
            directions.append([current_xy[0] - 2, current_xy[1]])
        if y_m2 != -1 and self.walls[current_xy[0]][current_xy[1] - 2] == '1':
            directions.append([current_xy[0], current_xy[1] - 2])
        if x_p2 < height and self.walls[current_xy[0] + 2][current_xy[1]] == '1':
            directions.append([current_xy[0] + 2, current_xy[1]])
        if y_p2 < width and self.walls[current_xy[0]][current_xy[1] + 2] == '1':
            directions.append([current_xy[0], current_xy[1] + 2])

        return directions

    def change_walls(self, current_xy, move_to):
        if move_to == "down":
            self.walls[current_xy[0] + 1][current_xy[1]] = '0'
            self.walls[current_xy[0] + 2][current_xy[1]] = '0'
        if move_to == "up":
            self.walls[current_xy[0] - 1][current_xy[1]] = '0'
            self.walls[current_xy[0] - 2][current_xy[1]] = '0'
        if move_to == "right":
            self.walls[current_xy[0]][current_xy[1] + 1] = '0'
            self.walls[current_xy[0]][current_xy[1] + 2] = '0'
        if move_to == "left":
            self.walls[current_xy[0]][current_xy[1] - 1] = '0'
            self.walls[current_xy[0]][current_xy[1] - 2] = '0'


    def get_dead_end_direction(self, current_xy, height, width):
        directions = []

        x_p2 = current_xy[0] + 2
        x_m2 = current_xy[0] - 2
        y_p2 = current_xy[1] + 2
        y_m2 = current_xy[1] - 2

        if x_m2 != -1 and self.walls[current_xy[0] - 1][current_xy[1]] == '1':
            directions.append([current_xy[0] - 2, current_xy[1]])
        if y_m2 != -1 and self.walls[current_xy[0]][current_xy[1] - 1] == '1':
            directions.append([current_xy[0], current_xy[1] - 2])
        if x_p2 < height and self.walls[current_xy[0] + 1][current_xy[1]] == '1':
            directions.append([current_xy[0] + 2, current_xy[1]])
        if y_p2 < width and self.walls[current_xy[0]][current_xy[1] + 1] == '1':
            directions.append([current_xy[0], current_xy[1] + 2])

        return directions

    def get_food(self, height, width):
        self.food = [['0' for j in range(width)] for i in range(height)]
        walls_copy = copy.deepcopy(self.walls)
        self.food_amount = 0


        for line in walls_copy:
            for elem in line:
                if walls_copy[walls_copy.index(line)][line.index(elem)] == '0':
                    self.food[walls_copy.index(line)][line.index(elem)] = '1'
                    walls_copy[walls_copy.index(line)][line.index(elem)] = '1'
                    self.food_amount+=1

        self.food[6][10] = '0'
        self.food[6][11] = '0'
        self.food[6][12] = '0'

        self.food[7][9] = '0'
        self.food[7][10] = '0'
        self.food[7][11] = '0'
        self.food[7][12] = '0'
        self.food[7][13] = '0'

        self.food_amount -= 8

        return self.food

    def add_ghost_home(self):
        x = [5, 6, 7, 8, 9]
        y = [7, 8, 9, 10, 11, 12, 13, 14, 15]
        y_in = [9, 10, 11, 12, 13]
        y_in2 = [10, 11, 12]

        for i in x:
            self.walls[i][8] = '1'
            self.walls[i][14] = '1'
        for j in y:
            self.walls[6][j] = '1'
            self.walls[8][j] = '1'

        for i in x:
            self.walls[i][7] = '0'
            self.walls[i][15] = '0'
        for j in y:
            self.walls[5][j] = '0'
            self.walls[9][j] = '0'

        for j in y_in2:
            self.walls[6][j] = '0'

        for j in y_in:
            self.walls[7][j] = '0'


