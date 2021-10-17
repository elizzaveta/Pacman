import copy

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

    def if_directions_opposite(self, directions):
        if len(directions) > 2:
            return False

        if "left" in directions and "right" in directions:
            return True

        if "up" in directions and "down" in directions:
            return True

        return False

    def find_graph_nodes(self):
        walls_copy = copy.deepcopy(self.walls)

        nodes = []

        y_in = [9, 10, 11, 12, 13]
        y_in2 = [10, 11, 12]


        for j in y_in2:
            walls_copy[6][j] = '1'

        for j in y_in:
            walls_copy[7][j] = '1'

        for line in walls_copy:
            for elem in line:
                if walls_copy[walls_copy.index(line)][line.index(elem)] == '0':

                    x = walls_copy.index(line)
                    y = line.index(elem)
                    if x == 5 and y ==1:
                        print("here")
                    directions = self.get_possible_directions_for_walls_copy(walls_copy.index(line), line.index(elem), 6)
                    if (not self.if_directions_opposite(directions)) and walls_copy.index(line) != 0 and line.index(elem) != 0 and line.index(elem) != self.width and walls_copy.index(line) != self.height:
                        nodes.append([walls_copy.index(line), line.index(elem)])
                    walls_copy[walls_copy.index(line)][line.index(elem)] = '1'


        return nodes

    def get_possible_directions_for_walls_copy(self, x, y, home_enter_ind):
        directions = []
        if self.walls[x][y-1] == '0':
            directions.append("left")
        if self.walls[x][y+1] == '0':
            directions.append("right")
        if self.walls[x-1][y] == '0':
            directions.append("up")
        if self.walls[x+1][y] == '0' and (x+1 != home_enter_ind and y !=10 or y !=11 and y != 12):
            directions.append("down")
        return directions

