""" read arrays from text files """


def read_2d_array(name):  # pacman_grid.txt
    with open(name) as textFile:
        lines = [line.split() for line in textFile]
    return lines


""" get direction in string format """
def get_direction(current_xy, new_xy):
    if current_xy[0] - new_xy[0] < 0:
        return "down"
    if current_xy[0] - new_xy[0] > 0:
        return "up"
    if current_xy[1] - new_xy[1] < 0:
        return "right"
    return "left"





# def read_into_array(name): #pacman_grid.txt
#     with open(name) as textFile:
#         lines = textFile.read().splitlines()
#     textFile.close()
#     return lines
#
# def string_to_bool(array):
#     new_arr = [[False for j in range(11)] for i in range(20)]
#     print("here")
#     for line in array:
#         for elem in line:
#             if elem == 'True':
#                 new_arr[array.index(line)][line.index(elem)] = True
#                 array[array.index(line)][line.index(elem)] = 'False'
#     return new_arr
#
# def reverse_string_ft_array(array):
#     for line in array:
#         for elem in line:
#             if elem == 'True':
#                 array[array.index(line)][line.index(elem)] = 'False'
#             else:
#                 array[array.index(line)][line.index(elem)] = 'True'
#     return array
#
