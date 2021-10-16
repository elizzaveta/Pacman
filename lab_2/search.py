"""
        algorithms

"""

def dfs(walls, start_xy, end_xy):
    best_path = []
    best_path_length = [100]

    def dfs_loop(walls, visited, current_xy, end_xy, current_path_length, current_path, best_path_length, best_path):
        visited.append(current_xy)
        current_path.append(current_xy)
        current_path_length[0] += 1

        adjacent_points = get_adjacent_points(walls, current_xy)

        for point in adjacent_points:
            if point not in visited:
                if point == end_xy or current_path_length[0] > best_path_length[0]:
                    if current_path_length[0] < best_path_length[0] and point == end_xy:
                        best_path_length[0] = current_path_length[0]
                        best_path[:] = current_path
                    break
                dfs_loop(walls, visited, point, end_xy, current_path_length, current_path, best_path_length, best_path)

        visited.pop(visited.index(current_xy))
        current_path.pop()
        current_path_length[0] -= 1

    dfs_loop(walls, [], start_xy, end_xy, [0], [], best_path_length, best_path)
    best_path.append(end_xy)
    return best_path


def bfs(walls, current_xy, end_xy):
    visited = [[current_xy, 0]]

    queue = [[current_xy, 0]]
    while len(queue) > 0:
        next_point = queue.pop(0)
        adjacent_points = get_bfs_adjacent_points(walls, next_point, False)
        for point in adjacent_points:
            if point not in visited:
                queue.append(point)
                visited.append(point)
                if point[0] == end_xy:
                    return get_bfs_path(walls, visited, current_xy, point, point[1])


def ucs(walls, food, start_xy, end_xy):
    start_node = [0, start_xy]
    queue = [start_node]
    visited = []
    path = []

    while queue:
        queue = sorted(queue)
        current_node = queue.pop()

        if current_node[1] == end_xy:

            visited.append(current_node[1])
            return get_ucs_path(path, start_xy, end_xy, current_node[0])

        if current_node[1] not in visited:
            adjacent_points = get_adjacent_points(walls, current_node[1])
            for point in adjacent_points:
                if point not in visited:
                    queue.append([(current_node[0] + int(food[point[0]][point[1]])), point])
                    path.append(
                        [current_node[0], (current_node[0] + int(food[point[0]][point[1]])), current_node[1], point])

        visited.append(current_node[1])


def get_adjacent_points(walls, current_xy):
    adjacent_points = []
    if walls[current_xy[0] - 1][current_xy[1]] == '0':
        adjacent_points.append([current_xy[0] - 1, current_xy[1]])
    if walls[current_xy[0] + 1][current_xy[1]] == '0':
        adjacent_points.append([current_xy[0] + 1, current_xy[1]])
    if walls[current_xy[0]][current_xy[1] - 1] == '0':
        adjacent_points.append([current_xy[0], current_xy[1] - 1])
    if walls[current_xy[0]][current_xy[1] + 1] == '0':
        adjacent_points.append([current_xy[0], current_xy[1] + 1])

    return adjacent_points


def get_bfs_adjacent_points(walls, current_bfs_xy, back):
    adjacent_points = []
    level = current_bfs_xy[1] + 1
    current_xy = current_bfs_xy[0]
    if back:
        level = current_bfs_xy[1] - 1
    if walls[current_xy[0] - 1][current_xy[1]] == '0':
        adjacent_points.append([[current_xy[0] - 1, current_xy[1]], level])
    if walls[current_xy[0] + 1][current_xy[1]] == '0':
        adjacent_points.append([[current_xy[0] + 1, current_xy[1]], level])
    if walls[current_xy[0]][current_xy[1] - 1] == '0':
        adjacent_points.append([[current_xy[0], current_xy[1] - 1], level])
    if walls[current_xy[0]][current_xy[1] + 1] == '0':
        adjacent_points.append([[current_xy[0], current_xy[1] + 1], level])

    return adjacent_points

"""
        get path

"""


def get_ucs_path(path_archive, start_xy, end_xy, cost):
    path = [end_xy]
    while end_xy != start_xy:
        for move in path_archive:
            if move[3] == end_xy and cost == move[1]:
                path.append(move[2])
                end_xy = move[2]
                path_archive.pop(path_archive.index(move))
                cost = move[0]

    return path[::-1]


def get_bfs_path(walls, visited, start_xy, end_xy, end_level):
    path = [end_xy[0]]
    current_xy = end_xy[0]
    while current_xy != start_xy:
        adjacent_points = get_bfs_adjacent_points(walls, [current_xy, end_level], True)
        for point in adjacent_points:
            if point in visited and point[1] == end_level - 1:
                path.append(point[0])
                current_xy = point[0]
                visited.pop(visited.index(point))
                break
        end_level -= 1
    return path[::-1]



