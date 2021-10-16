import copy


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent = []
        self.is_visited = 0


# now graph is stored in a dictionary. key is graph node and value is a list of adjacent nodes
class A_star:

    def __init__(self, graph_coords, walls):
        self.graph = {}
        for coord in graph_coords:
            self.graph[str(coord)] = []
        self.get_graph_from_walls(walls, graph_coords)


    def get_graph_from_walls(self, walls, graph_coords):
        for graph_coord in graph_coords:
            point = copy.deepcopy(graph_coord)
            found_left = False
            found_down = False
            current_xy = copy.deepcopy(point)
            while (not found_left) and current_xy[1] != 22:  # <----------------------------- change to width-1
                if walls[current_xy[0]][current_xy[1]+1] == 1:
                   break
                if [current_xy[0], current_xy[1] + 1] in graph_coords:
                    print("here", str(point))
                    self.graph[str(point)].append([current_xy[0], current_xy[1] + 1])
                    self.graph[str([current_xy[0], current_xy[1] + 1])].append(point)
                    found_left = True
                current_xy[1] += 1

            current_xy = copy.deepcopy(point)
            while (not found_down) and current_xy[0] != 12:  # <----------------------------- change to height-1
                if walls[current_xy[0] +1][current_xy[1]] == 1:
                    break
                if [current_xy[0] + 1, current_xy[1]] in graph_coords:
                    self.graph[str(point)].append([current_xy[0] + 1, current_xy[1]])
                    self.graph[str([current_xy[0] + 1, current_xy[1]])].append(point)
                    found_down = True
                current_xy[0] += 1
