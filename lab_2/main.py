from game import *

if __name__ == '__main__':
    game = Game()
    # game.run()

    maze_generator = MazeGenerator(23,13)
    walls = maze_generator.generate_maze()
    print(walls)

    pygame.init()
    display_info = DisplayInfo()
    win = pygame.display.set_mode((display_info.display_width + 120, display_info.display_height + 50))

    display = Display()
    display.draw_generated_maze(win,pygame, display_info, walls)

    pygame.display.update()
    d = maze_generator.dead_end

    # display.draw_dead_end(win, display_info, d)
    # pygame.display.update()

    print("here")