import copy
from game import *
from regression import *

if __name__ == '__main__':
    # i = 0
    # while(i<50):
    #     game = Game(2, 2, "alpha-beta")
    #     game.run()
    #     i+=1

    lr = LRegression('statistics/pacman_game_statistics.csv')

    lr.predicted_vs_test_plot()
    lr.display_predicted_n_samples(5)
    lr.display_error()

