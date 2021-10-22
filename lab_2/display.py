import copy


SPEED = 38

class Display:

    """ draw game window: background, pacman, ghosts, food, score """
    def draw_window(self, win, grid, display_info, pacman, ghosts, pygame, score, path, nodes):
        if nodes is None:
            nodes = []
        if path is None:
            path = [[], []]
        win.fill((0,0,0))

        self.draw_generated_maze(win, pygame, grid.walls)

        self.draw_path_to_ghost(path[0], win, pygame, 0)
        self.draw_path_to_ghost(path[1], win, pygame, 1)
        self.draw_dead_end(win, pygame, nodes)

        self.draw_food(win, grid, display_info)

        win.blit(self.get_pacman_direction_image(pacman, display_info), (display_info.pacman_x, display_info.pacman_y))

        win.blit(self.get_ghost_direction_image(0, ghosts, display_info),
                 (display_info.ghost_x[0], display_info.ghost_y[0]))
        win.blit(self.get_ghost_direction_image(1, ghosts, display_info),
                 (display_info.ghost_x[1], display_info.ghost_y[1]))

        self.draw_score(win, pygame, score, display_info)


        pygame.display.update()

    def draw_path_to_ghost(self, path, win, pygame, ind):
        # if len(path) > 2:
        #     path.pop()
        #     path.pop()
        #     path.pop(0)

        for point in path:
            y = 41 + 26 + 38 * (point[1]-1)
            x = 39 + 26 + 38 * (point[0]-1)
            if ind == 0:
                pygame.draw.rect(win, (255, 255, 255), (y, x, 10, 10))
            else:
                pygame.draw.rect(win, (79, 75, 176), (y, x, 10, 10))

        pygame.display.update()

    """ draw food """
    def draw_food(self, win, grid, display_info):
        food_copy = copy.deepcopy(grid.food)
        for line in food_copy:
            for elem in line:
                if (food_copy[food_copy.index(line)][line.index(elem)] == '1'):
                    y = 41 + 29 + 38 * (line.index(elem) - 1)
                    x = 39 + 29 + 38 * (food_copy.index(line) - 1)
                    win.blit(display_info.food, (y, x, 4, 4))
                    food_copy[food_copy.index(line)][line.index(elem)] = '0'

    """ get pacman image according to move direction """
    def get_pacman_direction_image(self, pacman, display_info):
        if pacman.left:
            return display_info.pacman_img_left
        if pacman.right:
            return display_info.pacman_img_right
        if pacman.up:
            return display_info.pacman_img_up
        return display_info.pacman_img_down

    """ get ghosts images according to move direction """
    def get_ghost_direction_image(self, index, ghosts, display_info):
        if ghosts[index].left:
            return display_info.ghost_img_left[index]
        if ghosts[index].right:
            return display_info.ghost_img_right[index]
        if ghosts[index].up:
            return display_info.ghost_img_up[index]
        return display_info.ghost_img_down[index]

    """ draw game score """
    def draw_score(self, win, pygame, score, display_info):
        text = "Score: " + str(score)
        font = pygame.font.SysFont('Comic Sans MS', 24, bold=pygame.font.Font.bold)
        letter1 = font.render(text, False, (255, 255, 0))
        win.blit(letter1, (53, display_info.score_y))

    """ draw game over image and  game result"""
    def draw_game_over(self, win, display_info, pygame, if_win):
        win.fill((17, 14, 61))
        win.blit(display_info.game_over_img, ((display_info.display_width-331)/2, (display_info.display_height-137)/2))

        text = "You "
        if if_win:
            text += "win!"
        else:
            text += "lose!"

        font = pygame.font.SysFont('Comic Sans MS', 24, bold=pygame.font.Font.bold)
        letter1 = font.render(text, False, (255, 255, 0))
        win.blit(letter1, ((display_info.display_width-120)/2, (display_info.display_height+137)/2))

        pygame.display.update()

    def draw_generated_maze(self,win, pygame, walls):
        walls_copy = copy.deepcopy(walls)
        for i in walls_copy:
            for j in i:
                if walls_copy[walls_copy.index(i)][i.index(j)] == '1':
                    x = 41 + 29 + 38 * (walls_copy.index(i) - 1)
                    y = 39 + 29 + 38 * (i.index(j) - 1)

                    dot = True

                    if i.index(j)+1 < len(i) and walls_copy[walls_copy.index(i)][i.index(j)+1] == '1':
                        dot = False
                        pygame.draw.rect(win, (64, 128, 255),(y, x, 38, 6))
                    if walls_copy.index(i) +1 < len(walls) and walls_copy[walls_copy.index(i)+1][i.index(j)] == '1':
                        dot = False
                        pygame.draw.rect(win, (64, 128, 255), (y, x, 6, 38))
                    if dot:
                        pygame.draw.rect(win, (64, 128, 255), (y, x, 6, 6))

                    walls_copy[walls_copy.index(i)][i.index(j)] = '0'

    def draw_food_copy(self, win, display_info, food):
        food_copy = copy.deepcopy(food)
        for line in food_copy:
            for elem in line:
                if (food_copy[food_copy.index(line)][line.index(elem)] == 1):
                    y = 41 + 29 + 38 * (line.index(elem) - 1)
                    x = 39 + 29 + 38 * (food_copy.index(line) - 1)
                    win.blit(display_info.food, (y, x, 4, 4))
                    food_copy[food_copy.index(line)][line.index(elem)] = 0

    def draw_dead_end(self, win, pygame, dead_ends):
        for end in dead_ends:
            x = 41 + 29 + 38 * (end[0] - 1)
            y = 39 + 29 + 38 * (end[1] - 1)
            pygame.draw.rect(win, (240, 0, 0), (y, x, 8, 8))

        pygame.display.update()