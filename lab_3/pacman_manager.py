

class PacmanManager:

    def __init__(self):
        self.current_state = "up"
        self.next_state = "up"

    """ puts next pressed key in sort of a queue """
    def key_pressed(self, direction):
        self.next_state = direction

    """ moves pacman """
    def move_pacman(self, game, pacman, grid, display_info):
        keep = grid.if_move_possible(pacman.x, pacman.y, self.current_state)
        new_dir = grid.if_move_possible(pacman.x, pacman.y, self.next_state)

        if new_dir:
            pacman.move_pacman_to(self.next_state, display_info)
            game.one_move(self.next_state)
            self.current_state = self.next_state
        elif keep:
            pacman.move_pacman_to(self.current_state, display_info)
            game.one_move(self.current_state)
