import time

import pygame
from layout import *
from agents import *
from display import *
from pacman_manager import *
from search import *
from maze_generator import *
from a_star import *
import random
import time

MAZE_WIDTH = 23
MAZE_HEIGHT = 13
PACMAN_START = [9, 9]
GHOST1_START = [7, 9]
GHOST2_START = [7, 13]

"""
display_info ghost y x, pacman y x. make automatic
game over photo
"""

class Game:

    def __init__(self):
        self.pacman = Pacman(0, PACMAN_START[0], PACMAN_START[1])
        self.pacman_manager = PacmanManager()
        self.ghosts = [Ghost(1, GHOST1_START[0], GHOST1_START[1]), Ghost(2, GHOST2_START[0], GHOST2_START[1])]
        self.maze_generator = MazeGenerator()
        self.grid = self.maze_generator.get_generated_grid(MAZE_HEIGHT, MAZE_WIDTH)
        # self.grid = Grid(20, 11, read_2d_array("layout/walls.txt"), read_2d_array("layout/food.txt"))
        self.display_info = DisplayInfo(MAZE_HEIGHT, MAZE_WIDTH)
        self.display = Display()
        self.score = 0
        self.win = 0
        self.keys_pressed = []
        self.clock = pygame.time.Clock()
        self.iterations = 0
        self.overall_time_dfs = 0
        self.overall_time_bfs = 0
        self.overall_time_ucs = 0


    """ main game function. Checks if game is over, calls agent move methods and methods drawing graphic elements on screen """
    def run(self):
        pygame.init()
        win = pygame.display.set_mode((self.display_info.display_width, self.display_info.display_height))
        self.display.draw_window(win, self.grid, self.display_info, self.pacman, self.ghosts, pygame, self.score, [[], []])
        nodes = self.grid.find_graph_nodes()
        a_star = A_star(nodes, self.grid.walls)
        # print(a_star.graph)

        # self.display.draw_dead_end(win, pygame, nodes)

        run = True
        while run:
            pygame.time.delay(170)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            """ make one pacman move """
            self.run_pacman_fine()

            """ chek if game over """
            if self.if_game_over():
                break

            # algorithm = "ucs"
            # path = self.run_path_algorithms_with_time(algorithm, 0)
            # path2 = self.run_path_algorithms_with_time(algorithm, 1)

            """ make one ghosts move """
            # self.run_ghosts_on_path([path, path2])
            self.run_ghosts()

            self.display.draw_window(win, self.grid, self.display_info, self.pacman, self.ghosts, pygame, self.score, [[], []])

            if self.if_game_over():
                break

        # self.display.draw_game_over(win, self.display_info, pygame, self.win)

        # print("Average dfs time: ", self.overall_time_dfs/self.iterations)
        # print("Average bfs time: ", self.overall_time_bfs/self.iterations)
        # print("Average ucs time: ", self.overall_time_ucs/self.iterations)
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

    def run_path_algorithms_with_time(self, algorithm, ghost_index):
        self.iterations += 1

        start = time.time()
        dfs_path = self.path_search_manager("dfs", ghost_index)
        self.overall_time_dfs += time.time() - start
        start = time.time()
        bfs_path = self.path_search_manager("bfs", ghost_index)
        self.overall_time_bfs += time.time() - start

        start = time.time()
        ucs_path = self.path_search_manager("ucs", ghost_index)
        self.overall_time_ucs += time.time() - start

        if algorithm == "dfs":
            return dfs_path
        if algorithm == "bfs":
            return bfs_path
        return ucs_path



    """ get path using given algorithm to the ghost """
    def path_search_manager(self, algorithm, ghost_index):
        if algorithm == "dfs":
            return dfs(self.grid.walls, [self.pacman.x, self.pacman.y], [self.ghosts[ghost_index].x, self.ghosts[ghost_index].y])

        if algorithm == "bfs":
            return bfs(self.grid.walls, [self.pacman.x, self.pacman.y], [self.ghosts[ghost_index].x, self.ghosts[ghost_index].y])

        return ucs(self.grid.walls, self.grid.food, [self.pacman.x, self.pacman.y],
                   [self.ghosts[ghost_index].x, self.ghosts[ghost_index].y])


    """ change game state according to one pacman move """
    def one_move(self, direction):
        self.score += int(self.grid.food[self.pacman.x][self.pacman.y])
        self.grid.food[self.pacman.x][self.pacman.y] = '0'
        self.pacman.change_direction(direction)

    """ check if game over """
    def if_game_over(self):
        if self.score == self.grid.food_amount:
            self.win = True
            return True
        if self.if_pacman_met_ghost():
            self.win = False
            return True
        return False

    """ check if pacman met one of the ghosts """
    def if_pacman_met_ghost(self):
        for ghost in self.ghosts:
            if self.pacman.x == self.ghosts[ghost.player - 1].x and self.pacman.y == self.ghosts[ghost.player - 1].y:
                return True

    """ one move of each ghost """
    def run_ghosts(self):
        for ghost in self.ghosts:
            if True:
                moved_to = self.ghosts[self.ghosts.index(ghost)].get_direction()
                opposite_to = self.ghosts[self.ghosts.index(ghost)].get_opposite_direciton(moved_to)
                directions = self.grid.get_possible_directions_for_move(self.ghosts[self.ghosts.index(ghost)].x,
                                                                        self.ghosts[self.ghosts.index(ghost)].y)
                if self.grid.if_move_possible(self.ghosts[self.ghosts.index(ghost)].x,
                                                  self.ghosts[self.ghosts.index(ghost)].y, moved_to):
                    directions.remove(opposite_to)
                new_direction = random.choice(directions)
                self.ghosts[self.ghosts.index(ghost)].move_to(new_direction, self.display_info, self.ghosts.index(ghost))

    """ run ghosts according to found path """
    def run_ghosts_on_path(self, path):
        for ghost in self.ghosts:
            moved_to = self.ghosts[self.ghosts.index(ghost)].get_direction()
            opposite_to = self.ghosts[self.ghosts.index(ghost)].get_opposite_direciton(moved_to)
            directions = self.grid.get_possible_directions_for_move(self.ghosts[self.ghosts.index(ghost)].x,
                                                                    self.ghosts[self.ghosts.index(ghost)].y)
            if len(directions) > 2 or moved_to not in directions:
                current_path_index = path[self.ghosts.index(ghost)].index([ghost.x, ghost.y])
                new_direction = get_direction([ghost.x, ghost.y],path[self.ghosts.index(ghost)][current_path_index-1])
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



























    # def run_pacman(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_LEFT] and self.display_info.pacman_x > 42 and self.grid.if_move_possible(self.pacman.x, self.pacman.y, "left"):
    #         self.display_info.pacman_x -= self.display_info.speed
    #         self.pacman.y -= 1
    #         self.one_move("left")
    #     elif keys[pygame.K_RIGHT] and self.display_info.pacman_x < 780 - self.display_info.pacman_width - 39 and self.grid.if_move_possible(self.pacman.x, self.pacman.y,"right"):
    #         self.display_info.pacman_x += self.display_info.speed
    #         self.pacman.y += 1
    #         self.one_move("right")
    #     elif keys[pygame.K_DOWN] and self.display_info.pacman_y < 485 - self.display_info.pacman_height - 86 and self.grid.if_move_possible(self.pacman.x, self.pacman.y,"down"):
    #         self.display_info.pacman_y += self.display_info.speed
    #         self.pacman.x += 1
    #         self.one_move("down")
    #     elif keys[pygame.K_UP] and self.display_info.pacman_y > 38 and self.grid.if_move_possible(self.pacman.x, self.pacman.y, "up"):
    #         self.display_info.pacman_y -= self.display_info.speed
    #         self.pacman.x -= 1
    #         self.one_move("up")
