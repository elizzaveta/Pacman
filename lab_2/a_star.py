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
        self.graph_nodes = graph_coords
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
                a = [current_xy[0], current_xy[1]+1]
                if walls[current_xy[0]][current_xy[1]+1] == '1':
                    break
                if [current_xy[0], current_xy[1] + 1] in graph_coords:
                    self.graph[str(point)].append([current_xy[0], current_xy[1] + 1])
                    self.graph[str([current_xy[0], current_xy[1] + 1])].append(point)
                    found_left = True
                current_xy[1] += 1

            current_xy = copy.deepcopy(point)
            while (not found_down) and current_xy[0] != 12:  # <----------------------------- change to height-1
                if walls[current_xy[0] +1][current_xy[1]] == '1':
                    break
                if [current_xy[0] + 1, current_xy[1]] in graph_coords:
                    self.graph[str(point)].append([current_xy[0] + 1, current_xy[1]])
                    self.graph[str([current_xy[0] + 1, current_xy[1]])].append(point)
                    found_down = True
                current_xy[0] += 1

    def get_cost_from_node_to_node(self, current_xy, new_xy, food):  # <----------------------------- make less code
        cost = 0
        x = current_xy[0]
        y = current_xy[1]
        if current_xy[0] == new_xy[0]:  # goes to left or right
            if current_xy[1] - new_xy[1] < 0:  # goes to right
                while y != new_xy[1]:
                    y += 1
                    if food[x][y] == '1':
                        cost += 1
                    else:
                        cost += 2
            else:  # goes to left
                while y != new_xy[1]:
                    y -= 1
                    if food[x][y] == '1':
                        cost += 1
                    else:
                        cost += 2
        else:  # goes up or down
            if current_xy[0] - new_xy[0] < 0:  # goes down
                while x != new_xy[0]:
                    x += 1
                    if food[x][y] == '1':
                        cost += 1
                    else:
                        cost += 2
            else:  # goes up
                while x != new_xy[0]:
                    x -= 1
                    if food[x][y] == '1':
                        cost += 1
                    else:
                        cost += 2
        return cost

    def a_star_search(self, start_xy, end_xy, food):
        open_nodes = []
        closed_nodes = []
        nodes_info = {}
        current_xy = start_xy
        h = self.get_heuristic_manhattan_distance(start_xy, end_xy)
        f = 0 + h
        nodes_info[str(start_xy)] = [f, []]

        while current_xy != end_xy:
            adjacent = self.graph[str(current_xy)]
            for node in adjacent:
                node_g = self.get_g_value(current_xy, node, start_xy, nodes_info, food)  # Calculate distance from start
                node_h = self.get_heuristic_manhattan_distance(node, end_xy)
                node_f = node_g + node_h
                if node not in open_nodes and node not in closed_nodes:
                    open_nodes.append(node)
                    nodes_info[str(node)] = [node_f, current_xy]

                if node_f <= f:
                    f = node_f
                    nodes_info[str(node)] = [node_f, current_xy]
            closed_nodes.append(current_xy)
            current_xy = self.find_new_current_from_open(open_nodes, nodes_info)
            open_nodes.pop(open_nodes.index(current_xy))


        print("Done!")

        return self.find_path(nodes_info, end_xy, start_xy)

    def get_g_value(self, current_xy, node, start_xy, nodes_info, food):
        g = 0
        g += self.get_cost_from_node_to_node(current_xy, node, food)

        while current_xy != start_xy:
            parent = nodes_info[str(current_xy)][1]
            cost = self.get_cost_from_node_to_node(current_xy, parent, food)
            g += cost
            current_xy = parent
        return g

    def find_new_current_from_open(self, open_nodes, nodes_info):
        nodes_info_copy = copy.deepcopy(nodes_info)
        new_current = []
        found = False
        while not found:
            min_node_key_temp = min(nodes_info_copy.items(), key=lambda x: x[1][0])[0]
            min_node_key = min_node_key_temp[1:-1].split(',')
            current_xy = [int(min_node_key[0]), int(min_node_key[1])]
            if current_xy not in open_nodes:
                del nodes_info_copy[min_node_key_temp]
            else:
                new_current = current_xy
                found = True
        return new_current


    def get_heuristic_manhattan_distance(self, current_xy, end_xy):
        return abs(current_xy[0] - end_xy[0]) + abs(current_xy[1] - end_xy[1])

    def find_path(self, nodes_info, end_xy, start_xy):
        path = [end_xy]
        current_xy = nodes_info[str(end_xy)][1]
        while current_xy != start_xy:
            path.append(current_xy)
            current_xy = nodes_info[str(current_xy)][1]
        path.append(current_xy)
        return path








