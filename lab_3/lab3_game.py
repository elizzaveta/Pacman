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
MAZE_HEIGHT = 15
PACMAN_START = [9, 9]
GHOST1_START = [7, 9]
GHOST2_START = [7, 13]


class Game_lab3:

    def __init__(self):
        self.pacman = Pacman(0, PACMAN_START[0], PACMAN_START[1])
        self.pacman_manager = PacmanManager()
        self.ghosts = [Ghost(1, GHOST1_START[0], GHOST1_START[1]), Ghost(2, GHOST2_START[0], GHOST2_START[1])]
        self.maze_generator = MazeGenerator()
        self.grid = self.maze_generator.get_generated_grid(MAZE_HEIGHT, MAZE_WIDTH)
        self.display_info = DisplayInfo(MAZE_HEIGHT, MAZE_WIDTH)
        self.display = Display()
        self.score = 0
        self.win = 0
        self.keys_pressed = []
        self.clock = pygame.time.Clock()
        self.iterations = 0
        self.house_closed = False

    """ main game function. Checks if game is over, calls agent move methods and methods drawing graphic elements on screen """

    def run(self):
        pygame.init()
        win = pygame.display.set_mode((self.display_info.display_width, self.display_info.display_height))
        self.display.draw_window(win, self.grid, self.display_info, self.pacman, self.ghosts, pygame, self.score,
                                 [[], []])

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

            self.close_house()

            """ make one ghosts move """
            self.run_a_star(win)

            """ display game state"""
            self.display.draw_window(win, self.grid, self.display_info, self.pacman, self.ghosts, pygame, self.score)

            """ chek if game over """
            if self.if_game_over():
                break

        self.display.draw_game_over(win, self.display_info, pygame, self.win)
        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


    def close_house(self):
        if not self.house_closed:
            closed = self.grid.close_house([self.pacman.x, self.pacman.y], [self.ghosts[0].x, self.ghosts[0].y],
                                           [self.ghosts[1].x, self.ghosts[1].y])
            if closed:
                self.house_closed = True

    def run_a_star(self, win):
        if self.house_closed:
            nodes = self.grid.find_graph_nodes()
            nodes.append([self.pacman.x, self.pacman.y])
            nodes.append([self.ghosts[0].x, self.ghosts[0].y])
            nodes.append([self.ghosts[1].x, self.ghosts[1].y])
            a_star = A_star(nodes, self.grid.walls)
            # "manhattan" "euclidean" "greedy"
            a_path1 = a_star.a_star_search([self.pacman.x, self.pacman.y], [self.ghosts[0].x, self.ghosts[0].y],
                                           self.grid.food, "manhattan")
            a_path2 = a_star.a_star_search([self.pacman.x, self.pacman.y], [self.ghosts[1].x, self.ghosts[1].y],
                                           self.grid.food, "greedy")
            path1 = self.make_path_from_graph_path(a_path1)
            path2 = self.make_path_from_graph_path(a_path2)

            self.display.draw_dead_end(win, pygame, path1)
            self.run_ghosts_on_path([path1, path2])
        else:
            self.run_ghosts()



    """ get path using given algorithm to the ghost """

    def path_search_manager(self, algorithm, ghost_index):
        if algorithm == "dfs":
            return dfs(self.grid.walls, [self.pacman.x, self.pacman.y],
                       [self.ghosts[ghost_index].x, self.ghosts[ghost_index].y])

        if algorithm == "bfs":
            return bfs(self.grid.walls, [self.pacman.x, self.pacman.y],
                       [self.ghosts[ghost_index].x, self.ghosts[ghost_index].y])

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
                self.ghosts[self.ghosts.index(ghost)].move_to(new_direction, self.display_info,
                                                              self.ghosts.index(ghost))

    """ run ghosts according to found path """

    def run_ghosts_on_path(self, path):
        for ghost in self.ghosts:
            moved_to = self.ghosts[self.ghosts.index(ghost)].get_direction()
            opposite_to = self.ghosts[self.ghosts.index(ghost)].get_opposite_direciton(moved_to)
            directions = self.grid.get_possible_directions_for_move(self.ghosts[self.ghosts.index(ghost)].x,
                                                                    self.ghosts[self.ghosts.index(ghost)].y)
            if len(directions) > 2 or moved_to not in directions:
                current_path_index = path[self.ghosts.index(ghost)].index([ghost.x, ghost.y])
                new_direction = get_direction([ghost.x, ghost.y],
                                              path[self.ghosts.index(ghost)][current_path_index + 1])
                self.ghosts[self.ghosts.index(ghost)].move_to(new_direction, self.display_info,
                                                              self.ghosts.index(ghost))
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
