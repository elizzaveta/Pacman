import time

import pygame
from layout import *
from game.agents import *
from maze.display import *
from game.pacman_manager import *
from algorithms.search import *
from maze.maze_generator import *
from statistics import *
from algorithms.a_star import *
from algorithms.expectimax import *
import random


MAZE_WIDTH = 20
MAZE_HEIGHT = 11
PACMAN_START = [9, 9]
GHOST1_START = [5, 8]
GHOST2_START = [5, 11]
GHOST3_START = [7, 10]
GHOST4_START = [7, 12]


class Game:

    def __init__(self):
        self.pacman = Pacman(0, PACMAN_START[0], PACMAN_START[1])
        self.pacman_manager = PacmanManager()
        self.ghosts = self.init_ghosts(1, 2)
        self.maze_generator = MazeGenerator()
        # self.grid = Grid(5, 5, read_2d_array("layout/walls_55.txt"), read_2d_array("layout/food_55.txt"), 24)
        self.grid = Grid(20, 11, read_2d_array("../layout/walls.txt"), read_2d_array("../layout/food.txt"), 99)
        self.grid.food[PACMAN_START[0]][PACMAN_START[1]]= '0'
        self.display_info = DisplayInfo(MAZE_HEIGHT, MAZE_WIDTH)
        self.display = Display()
        self.statistics = Statistics()
        self.score = 0
        self.if_win = True
        self.keys_pressed = []
        self.house_closed = False
        self.algorithm = "alpha-beta"
        self.prev = [[1, 1], [1, 1]]
        self.minimax = Minimax(self.grid.food_amount, self.grid, "alpha-beta", 0.5)
        self.win = pygame.display.set_mode((self.display_info.display_width, self.display_info.display_height))


    def reset(self):
        self.__init__()

    """ initiate ghosts according to given parameters """
    def init_ghosts(self, num_of_ghosts_type1, num_of_ghosts):
        if num_of_ghosts_type1 > 4: num_of_ghosts_type1 = 4
        if num_of_ghosts > 4: num_of_ghosts = 4
        start_pos = [GHOST1_START, GHOST2_START, GHOST3_START, GHOST4_START]
        ghosts = []

        for i in range(num_of_ghosts_type1):
            ghosts.append(Ghost(i+1, start_pos[i][0], start_pos[i][1], "search"))

        for i in range(num_of_ghosts-num_of_ghosts_type1):
            j = i + num_of_ghosts_type1
            ghosts.append(Ghost(j+1, start_pos[j][0], start_pos[j][1], "random"))

        return ghosts

    def display_state(self):
        self.display.draw_window(self.win, self.grid, self.display_info, self.pacman, self.ghosts, pygame, self.score,
                                 [[], []], [])

    """ main game function. Checks if game is over, calls agent move methods and methods drawing graphic elements on screen """
    def run(self):
        pygame.init()
        self.display_state()
        start_time = time.time()

        run = True
        while run:
            pygame.time.delay(180)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False



            """ make one ghosts move """
            self.run_ghosts(0.6)


            """ chek if game over """
            if self.if_game_over():
                break

            # self.close_house()

            """ make one pacman move """
            # self.run_pacman_fine()

            ghosts_xy =[]
            for ghost in self.ghosts:
                ghosts_xy.append([ghost.x, ghost.y])
            prev = self.prev.pop(0)
            p_dir = self.minimax.run( prev, self )
            p_xy = []

            if p_dir == "left":
                p_xy = [self.pacman.x, self.pacman.y-1]
            if p_dir == "right":
                p_xy = [self.pacman.x, self.pacman.y+1]
            if p_dir == "up":
                p_xy = [self.pacman.x-1, self.pacman.y]
            if p_dir == "down":
                p_xy = [self.pacman.x+1, self.pacman.y]

            self.prev.append(p_xy)
            self.run_pacman_on_path([[self.pacman.x, self.pacman.y], p_xy])

            """ display game state"""
            self.display_state()

            """ chek if game over """
            if self.if_game_over():
                break





        self.statistics.add_statistics(self.if_win, time.time() - start_time, abs(self.score), self.algorithm)
        self.display.draw_game_over(self.win, self.display_info, pygame, self.if_win)
        # while run:
        #     pygame.time.delay(100)
        #
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             run = False

    def distance_to_ghosts(self):
        return (abs(self.pacman.x - self.ghosts[0].x) + abs(self.pacman.y - self.ghosts[0].y)
    +abs(self.pacman.x - self.ghosts[1].x) + abs(self.pacman.y - self.ghosts[1].y))

    def run_for_dqn(self, action_item):


        """ make one ghosts move """
        self.run_ghosts(0.6)
        # self.run_ghosts_random(self.ghosts[0])
        # self.run_ghosts_random(self.ghosts[1])

        done = self.if_game_over()
        if(done): return done

        self.run_pacman_to_dir(action_item)
        """ display game state"""

        done = (done or self.if_game_over())

        return done



    """ change game state according to one pacman move """
    def one_move(self, direction):
        self.score += int(self.grid.food[self.pacman.x][self.pacman.y])
        self.grid.food[self.pacman.x][self.pacman.y] = '0'
        self.pacman.change_direction(direction)

    """ check if game over """
    def if_game_over(self):
        if self.score == self.grid.food_amount-1:
            self.if_win = True
            return True
        if self.if_pacman_met_ghost():
            self.if_win = False
            self.score = self.score
            return True
        return False

    """ check if pacman met one of the ghosts """
    def if_pacman_met_ghost(self):
        for ghost in self.ghosts:
            if self.pacman.x == self.ghosts[ghost.player - 1].x and self.pacman.y == self.ghosts[ghost.player - 1].y:
                return True

    """ one move of each ghost """
    def run_ghosts(self, accuracy_of_search):
        for ghost in self.ghosts:
            if ghost.type == 'random':
                self.run_ghosts_random(ghost)
            elif ghost.type == 'search':
                rnd = random.random()
                if rnd<accuracy_of_search:
                    self.run_ghosts_search(ghost)
                else:
                    self.run_ghosts_random(ghost)





    def run_ghosts_random(self, ghost):
        moved_to = self.ghosts[self.ghosts.index(ghost)].get_direction()
        opposite_to = self.ghosts[self.ghosts.index(ghost)].get_opposite_direciton(moved_to)
        directions = self.grid.get_possible_directions_for_move(self.ghosts[self.ghosts.index(ghost)].x,
                                                                self.ghosts[self.ghosts.index(ghost)].y)
        if self.grid.if_move_possible(self.ghosts[self.ghosts.index(ghost)].x,
                                      self.ghosts[self.ghosts.index(ghost)].y, moved_to):
            directions.remove(opposite_to)
        new_direction = random.choice(directions)
        self.ghosts[self.ghosts.index(ghost)].move_to(new_direction, self.display_info, self.ghosts.index(ghost))

    def run_ghosts_search(self, ghost):
        path = dfs(self.grid.walls, [ghost.x, ghost.y], [self.pacman.x, self.pacman.y])
        self.run_ghosts_on_path(path, ghost)

    """ run ghosts according to found path """
    def run_ghosts_on_path(self, path, ghost):
        moved_to = self.ghosts[self.ghosts.index(ghost)].get_direction()
        opposite_to = self.ghosts[self.ghosts.index(ghost)].get_opposite_direciton(moved_to)
        directions = self.grid.get_possible_directions_for_move(self.ghosts[self.ghosts.index(ghost)].x,
                                                                self.ghosts[self.ghosts.index(ghost)].y)
        if len(directions) > 2 or moved_to not in directions:
            current_path_index = path.index([ghost.x, ghost.y])
            new_direction = get_direction([ghost.x, ghost.y], path[current_path_index + 1])
            self.ghosts[self.ghosts.index(ghost)].move_to(new_direction, self.display_info, self.ghosts.index(ghost))
        else:
            if self.grid.if_move_possible(self.ghosts[self.ghosts.index(ghost)].x,
                                          self.ghosts[self.ghosts.index(ghost)].y, moved_to):
                directions.remove(opposite_to)

            new_direction = random.choice(directions)
            self.ghosts[self.ghosts.index(ghost)].move_to(new_direction, self.display_info,
                                                          self.ghosts.index(ghost))



    """ one move of pacman """
    def run_pacman_fine(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pacman_manager.key_pressed("left")
        elif keys[pygame.K_RIGHT]:
            self.pacman_manager.key_pressed("right")
        elif keys[pygame.K_DOWN]:
            self.pacman_manager.key_pressed("down")
        elif keys[pygame.K_UP]:
            self.pacman_manager.key_pressed("up")

        self.pacman_manager.move_pacman(self, self.pacman, self.grid, self.display_info)

    def run_pacman_to_dir(self, action_number):
        if action_number == 0:
            self.pacman_manager.key_pressed("down")
        elif action_number == 1:
            self.pacman_manager.key_pressed("up")
        elif action_number == 2:
            self.pacman_manager.key_pressed("left")
        elif action_number == 3:
            self.pacman_manager.key_pressed("right")


        if(action_number >=0 and action_number<=3):
            self.pacman_manager.move_pacman(self, self.pacman, self.grid, self.display_info)


    def run_pacman_on_path(self, path):
        current_xy = path[0]
        new_xy = path[1]
        direction = get_direction(current_xy, new_xy)
        if direction == "left":
            self.pacman_manager.key_pressed("left")
        elif direction == "right":
            self.pacman_manager.key_pressed("right")
        elif direction == "down":
            self.pacman_manager.key_pressed("down")
        elif direction == "up":
            self.pacman_manager.key_pressed("up")
        # path.pop(0)
        # if len(path) == 1:
        #     self.pacman_in_move = 0
        self.pacman_manager.move_pacman(self, self.pacman, self.grid, self.display_info)


    def make_path_from_graph_path(self, graph_path):
        path = []
        path.append(graph_path[0])
        graph_path.pop(0)

        current_xy = path[0]

        while len(graph_path) != 0:

            direction = get_direction(current_xy, graph_path[0])
            while current_xy != graph_path[0]:
                if direction == "left":
                    current_xy = [current_xy[0], current_xy[1] - 1]
                if direction == "right":
                    current_xy = [current_xy[0], current_xy[1] + 1]
                if direction == "up":
                    current_xy = [current_xy[0] - 1, current_xy[1]]
                if direction == "down":
                    current_xy = [current_xy[0] + 1, current_xy[1]]
                path.append(current_xy)
            graph_path.pop(0)

        return path
























