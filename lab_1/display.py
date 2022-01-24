import copy


class Display:

    """ draw game window: background, pacman, ghosts, food, score """
    def draw_window(self, win, grid, display_info, pacman, ghosts, pygame, score, path):
        win.blit(display_info.background, (0, 0))

        self.draw_path_to_ghost(path[0], win, pygame, 0)
        self.draw_path_to_ghost(path[1], win, pygame, 1)

        self.draw_food(win, grid, display_info)

        win.blit(self.get_pacman_direction_image(pacman, display_info), (display_info.pacman_x, display_info.pacman_y))

        win.blit(self.get_ghost_direction_image(0, ghosts, display_info),
                 (display_info.ghost_x[0], display_info.ghost_y[0]))
        win.blit(self.get_ghost_direction_image(1, ghosts, display_info),
                 (display_info.ghost_x[1], display_info.ghost_y[1]))

        self.draw_score(win, pygame, score)


        pygame.display.update()

    def draw_path_to_ghost(self, path, win, pygame, ind):
        if len(path) > 2:
            path.pop()
            path.pop()
            path.pop(0)

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
    def draw_score(self, win, pygame, score):
        text = "Score: " + str(score)
        font = pygame.font.SysFont('Comic Sans MS', 24, bold=pygame.font.Font.bold)
        letter1 = font.render(text, False, (255, 255, 0))
        win.blit(letter1, (53, 430))

    """ draw game over image and  game result"""
    def draw_game_over(self, win, display_info, pygame, if_win):
        win.blit(display_info.game_over_img, (0, 0))

        text = "You "
        if if_win:
            text += "win!"
        else:
            text += "lose!"

        font = pygame.font.SysFont('Comic Sans MS', 24, bold=pygame.font.Font.bold)
        letter1 = font.render(text, False, (255, 255, 0))
        win.blit(letter1, (320, 350))

        pygame.display.update()