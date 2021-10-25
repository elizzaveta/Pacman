import copy
from math import sqrt
from additional_functions import *

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
            while (not found_left) and current_xy[1] != len(walls[0]) - 1:
                if walls[current_xy[0]][current_xy[1] + 1] == '1':
                    break
                if [current_xy[0], current_xy[1] + 1] in graph_coords:
                    self.graph[str(point)].append([current_xy[0], current_xy[1] + 1])
                    self.graph[str([current_xy[0], current_xy[1] + 1])].append(point)
                    found_left = True
                current_xy[1] += 1

            current_xy = copy.deepcopy(point)
            while (not found_down) and current_xy[0] != len(walls) - 1:
                if walls[current_xy[0] + 1][current_xy[1]] == '1':
                    break
                if [current_xy[0] + 1, current_xy[1]] in graph_coords:
                    self.graph[str(point)].append([current_xy[0] + 1, current_xy[1]])
                    self.graph[str([current_xy[0] + 1, current_xy[1]])].append(point)
                    found_down = True
                current_xy[0] += 1

    def get_cost_from_node_to_node(self, current_xy, new_xy, food):
        cost = 0
        x = current_xy[0]
        y = current_xy[1]

        direction = get_direction(current_xy, new_xy)

        if current_xy[0] == new_xy[0]:
            while y != new_xy[1]:
                if direction == "right":
                    y += 1
                else:
                    y -= 1
                if food[x][y] == '1':
                    cost += 1
                else:
                    cost += 4
        else:
            while x != new_xy[0]:
                if direction == "down":
                    x += 1
                else:
                    x -= 1
                if food[x][y] == '1':
                    cost += 1
                else:
                    cost += 4

        return cost

    """ a star algorithm to find path from start_xy across all end nodes (n_end_xy) """
    """ using given heuristic parameter """
    """ if given one end node - classic a star alg """
    def a_star_search_n_dots(self, start_xy, n_end_xy, food, walls, heuristic):
        path = []
        current_xy = start_xy

        while len(n_end_xy) != 0:
            start_xy = current_xy
            n_end_xy = self.orderer_n_dots(n_end_xy, start_xy)
            end_xy = n_end_xy.pop(0)
            open_nodes = []
            closed_nodes = []
            nodes_info = {}
            f = 0 + self.get_heuristic(heuristic, start_xy, end_xy, walls)
            nodes_info[str(start_xy)] = [f, []]

            while current_xy != end_xy:
                adjacent = self.graph[str(current_xy)]
                for node in adjacent:
                    node_g = self.get_g_value(current_xy, node, start_xy, nodes_info, food)  # Calculate distance from start
                    node_h = self.get_heuristic(heuristic, node, end_xy, walls)
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
            path+= self.find_back_path(nodes_info, end_xy, start_xy)[::-1]
            for elem in path:
                food[elem[0]][elem[1]] = '0'
                if elem in n_end_xy: n_end_xy.remove(elem)

        return path

    """ order end nodes according to heuristic value """
    def orderer_n_dots(self, n_end_xy, start_xy):
        h_arr = []
        sorted = []
        for end_xy in n_end_xy:
            h = self.get_heuristic("manhattan", start_xy, end_xy, [])
            h_arr.append(h)
        for h in h_arr:
            min_h = min(h_arr)
            index = h_arr.index(min_h)
            h_arr[index] = 100
            sorted.append(n_end_xy[index])
        return sorted

    """ for a star: get weight between nodes """
    def get_g_value(self, current_xy, node, start_xy, nodes_info, food):
        g = 0
        g += self.get_cost_from_node_to_node(current_xy, node, food)

        while current_xy != start_xy:
            parent = nodes_info[str(current_xy)][1]
            cost = self.get_cost_from_node_to_node(current_xy, parent, food)
            g += cost
            current_xy = parent
        return g

    """ for a star: find node for next move from open nodes with minimal path value """
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

    """ get estimated heuristic value """
    def get_heuristic(self, method, current_xy, end_xy, walls):
        if method == "manhattan":
            return abs(current_xy[0] - end_xy[0]) + abs(current_xy[1] - end_xy[1])
        elif method == "euclidean":
            return sqrt((current_xy[0] - end_xy[0]) ** 2 + (current_xy[1] - end_xy[1]) ** 2)
        elif method == "greedy":
            return 0
        elif method == "s opt":
            return (abs(current_xy[0] - end_xy[0]) + abs(current_xy[1] - end_xy[1]) + self.count_walls_between_nodes(copy.deepcopy(current_xy), copy.deepcopy(end_xy), walls))

    """ estimate how many walls is on line from node to node """
    def count_walls_between_nodes(self, node1_xy, node2_xy, walls):
        x = abs(node1_xy[0] - node2_xy[0])
        y = abs(node1_xy[1] - node2_xy[1])
        if x > y:
            if int(y/2) == 0: y = 2
            node1_xy[1] = int(y/2)
            node2_xy[1] = int(y/2)
        else:
            if int(x/2) == 0: x = 2
            node1_xy[0] = int(x/2)
            node2_xy[0] = int(x/2)
        return self.count_walls_on_line(node1_xy, node2_xy, walls)

    def count_walls_on_line(self, node1_xy, node2_xy, walls):
        n_walls = 0
        if node1_xy[0] == node2_xy[0]:
            x = node1_xy[0]
            a = [node1_xy[1], node2_xy[1]]
            y1 = min([node1_xy[1], node2_xy[1]])
            y2 = max([node1_xy[1], node2_xy[1]])
            while y1 != y2:
                if walls[int(x)][y1] == '1':
                    n_walls+=1
                y1+=1
        else:
            y = node1_xy[1]
            x1 = min([node1_xy[0], node2_xy[0]])
            x2 = max([node1_xy[0], node2_xy[0]])
            while x1 != x2:
                if walls[x1][int(y)] == '1':
                    n_walls += 1
                x1 +=1
        return n_walls

    """ get found path """
    def find_back_path(self, nodes_info, end_xy, start_xy):
        path = [end_xy]
        current_xy = nodes_info[str(end_xy)][1]
        while current_xy != start_xy:
            path.append(current_xy)
            current_xy = nodes_info[str(current_xy)][1]
        path.append(current_xy)
        return path






    # old version
    def a_star_search(self, start_xy, end_xy, food,walls, heuristic):
        open_nodes = []
        closed_nodes = []
        nodes_info = {}
        current_xy = start_xy
        f = 0 + self.get_heuristic(heuristic, start_xy, end_xy, walls)
        nodes_info[str(start_xy)] = [f, []]

        while current_xy != end_xy:
            adjacent = self.graph[str(current_xy)]
            for node in adjacent:
                node_g = self.get_g_value(current_xy, node, start_xy, nodes_info, food)  # Calculate distance from start
                node_h = self.get_heuristic(heuristic, node, end_xy, walls)
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
        return self.find_back_path(nodes_info, end_xy, start_xy)
