import copy

from game import *
from lab3_game import *

if __name__ == '__main__':
    game = Game(1, 2, "expectimax")
    # algorithms: expectimax alpha-beta
    # first param is how many search agents
    # second - overal amount

    game.run()


