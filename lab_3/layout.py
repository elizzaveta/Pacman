import pygame.image


""" information about game display """
class DisplayInfo:

    def __init__(self, height, width):
        self.display_width = 26 + width * 38
        self.display_height = 45 + height * 38
        self.pacman_width = 41
        self.pacman_height = 41
        self.ghost_height = 40
        self.ghost_width = 40

        self.speed = 38
        self.score_y = self.display_height - 38
        self.pacman_x = 52 + 304 + 7 -38*8
        self.pacman_y = 48 + 304 + 7 - 38*8
        self.ghost_x = [48 + 266 + 6 + 38, 48 + 380 + 6 + 38*2, 48 + 266 + 6 + 38*2, 48 + 380 + 6 + 38]
        self.ghost_y = [286, 286, 286, 286]

        self.agents_x = [52 + 304 + 7, 48 + 266 + 6, 48 + 380 + 6]
        self.agents_y = [48 + 304 + 7, 52+152+6, 52+152+6]

        self.background = pygame.image.load("sprites/map.jpeg")
        self.game_over_img = pygame.image.load("sprites/game_over_sm.png")
        self.food = pygame.image.load("sprites/food.png")
        self.b_food = pygame.image.load("sprites/big food.png")

        self.pacman_img_left = pygame.image.load("sprites/pacman_l1.png")
        self.pacman_img_right = pygame.image.load("sprites/pacman_r1.png")
        self.pacman_img_up = pygame.image.load("sprites/pacman_u1.png")
        self.pacman_img_down = pygame.image.load("sprites/pacman_d1.png")

        self.ghost_img_left = [pygame.image.load("sprites/ghost1_left.png"), pygame.image.load("sprites/ghost2_left.png"), pygame.image.load("sprites/ghost3_left.png"), pygame.image.load("sprites/ghost4_left.png")]
        self.ghost_img_right = [pygame.image.load("sprites/ghost1_right.png"), pygame.image.load("sprites/ghost2_right.png"), pygame.image.load("sprites/ghost3_right.png"), pygame.image.load("sprites/ghost4_right.png")]
        self.ghost_img_up = [pygame.image.load("sprites/ghost1_up.png"), pygame.image.load("sprites/ghost2_up.png"), pygame.image.load("sprites/ghost3_up.png"), pygame.image.load("sprites/ghost4_up.png")]
        self.ghost_img_down = [pygame.image.load("sprites/ghost1_down.png"), pygame.image.load("sprites/ghost2_down.png"), pygame.image.load("sprites/ghost3_down.png"), pygame.image.load("sprites/ghost4_down.png")]

