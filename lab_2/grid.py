
class Grid:

    def __init__(self, width, height, walls, food, food_amount):
        self.width = width
        self.height = height
        self.walls = walls
        self.food = food
        self.food_amount = food_amount


    """ check if move from [x][y] is possible to given direction """
    def if_move_possible(self, x, y, direction):
        x_or_y = self.dir_x_or_y(direction)
        delta = self.dir_index(direction)

        new_coord = [x, y]
        if x_or_y == "x":
            new_coord[0] += delta
        else:
            new_coord[1] += delta

        if self.walls[new_coord[0]][new_coord[1]] == '1':
            return False
        return True

    """ get how coords should be changed according to move direction """
    def dir_index(self, dir):
        if dir == "left": return -1
        if dir == "right": return 1
        if dir == "up": return -1
        if dir == "down": return 1

    """ get which coord (x or y) should be chacged according to move direction """
    def dir_x_or_y(self, dir):
        if dir =="left": return "y"
        if dir == "right": return "y"
        if dir == "up" : return "x"
        if dir == "down" : return "x"

    """ get an array of all possible directions for a next move """
    def get_possible_directions_for_move(self, x, y):
        directions = []
        if self.walls[x][y-1] == '0':
            directions.append("left")
        if self.walls[x][y+1] == '0':
            directions.append("right")
        if self.walls[x-1][y] == '0':
            directions.append("up")
        if self.walls[x+1][y] == '0':
            directions.append("down")
        return directions

