from game.game import *

if __name__ == '__main__':
    # game = Game(1, 1, "alpha-beta")
    # game.run()
    pygame.init()
    print('start')
    game = Game()
    game.display_state()
    done = game.if_game_over()
    print('before loop')

    i = 0
    while(i<10):
        game.reset()
        j = 0
        while(j<10):
            done = game.run_for_dqn(4)
            game.display_state()
            j+=1
        i+=1

    # i = 0
    # while(i<50):
    #     game = Game(2, 2, "alpha-beta")
    #     game.run()
    #     i+=1

    # lr = LRegression('statistics/pacman_game_statistics.csv')
    #
    # lr.predicted_vs_test_plot()
    # lr.display_predicted_n_samples(5)
    # lr.display_error()

