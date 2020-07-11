'''
Add this file with 'from MapGenarator import *'
When you need a new map just write map = map_generator.generate_map()
This function returns new map as 2d array.
'#' - means wall
'O' - means free cell
'p1' and 'p2' - mean two portal cells on the map
'g' - means spawn point for ghosts. it has (0, 1) coords inside their 'house'
'''


import random
import pygame
from Variables import *

class MapGenerator:
    def __init__(self):
        self.width = 8
        self.height = 9

    def generate_map(self):
        map = self.make_skeleton()
        map = self.add_ghots_house(map)
        map = self.add_portals(map)
        map = self.thin_passages(map)
        map = self.fill_pockets(map)
        map = self.add_ghots_house(map)
        map = self.add_portals(map)
        map = self.move_dead_ends_to_edges(map)
        map = self.eleminate_dead_ends_on_edges(map)
        map = self.eleminate_extra_passages(map)

        if quality_check(map):
            map = self.convert_to_normal_type(map)
            return map
        else:
            map = self.generate_map()
            return map

    def convert_to_normal_type(self, map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    map[i][j] = '#'
                if map[i][j] == 0:
                    map[i][j] = 'O'
        map[15][0] = 'p1'
        map[15][27] = 'p2'
        map[15][11] = 'g'
        return map

    def eleminate_extra_passages(self, map):
        if quality_check(map):
            for i in range(1, len(map) // 2):
                for j in range(1, len(map[i]) // 2):
                    map_copy = copy_2d_array(map)
                    if map_copy[i][j] == 0:
                        mirror_change(map_copy, i, j, 1)
                        map_copy = self.fill_pockets(map_copy)
                        map_copy = self.add_ghots_house(map_copy)
                        map_copy = self.add_portals(map_copy)
                        if quality_check(map_copy):
                            map = map_copy
        return map

    def eleminate_dead_ends_on_edges(self, map):
        for j in range(1, len(map[0]) - 1):
            map = mirror_change(map, 1, j, 0)
            map = mirror_change(map, 2, j, 1)
        for i in range(2, 10):
            map = mirror_change(map, i, 1, 0)
            map = mirror_change(map, i, 2, 1)

        for j in range(2, len(map[0]) - 2):
            if map[3][j] == 0 and map[2][j - 1] == 1 and map[2][j + 1] == 1:
                map = mirror_change(map, 2, j, 0)
        for i in range(2, 10):
            if map[i][3] == 0 and map[i - 1][2] == 1 and map[i + 1][2] == 1:
                map = mirror_change(map, i, 2, 0)
        map = self.thin_passages(map)
        map = self.fill_pockets(map)
        map = self.add_ghots_house(map)
        map = self.add_portals(map)
        map = self.thin_passages(map)
        map = self.add_ghots_house(map)
        map = self.add_portals(map)
        return map

    def move_dead_ends_to_edges(self, map):
        for i in range(1, len(map) - 1):
            for j in range(1, len(map[i]) - 1):
                neighbors = count_neighbors(map, i, j)
                if neighbors == 3 and map[i][j] == 0:
                    next_cell_i = None
                    next_cell_j = None
                    if map[i + 1][j] == 0:
                        next_cell_i = i - 1
                        next_cell_j = j
                    elif map[i - 1][j] == 0:
                        next_cell_i = i + 1
                        next_cell_j = j
                    elif map[i][j + 1] == 0:
                        next_cell_i = i
                        next_cell_j = j - 1
                    elif map[i][j - 1] == 0:
                        next_cell_i = i
                        next_cell_j = j + 1
                    if next_cell_i > 0 and next_cell_i < len(map) - 1 and next_cell_j > 0 and next_cell_j < len(map[0]) - 1:
                        map = mirror_change(map, next_cell_i, next_cell_j, 0)
        return map


    def thin_passages(self, map):
        for i in range(1, len(map) - 2):
            for j in range(1, len(map[i]) - 2):
                if map[i][j] == 0 and map[i + 1][j] == 0 and map[i][j + 1] == 0 and map[i + 1][j + 1] == 0:
                    fill_x = None
                    fill_y = None
                    if i < 15:
                        fill_y = 0
                    else:
                        fill_y = 1
                    if j < 14:
                        fill_x = 0
                    else:
                        fill_x = 1
                    final_y = i + fill_y
                    final_x = j + fill_x
                    map = mirror_change(map, final_y, final_x, 1)
        return map

    def add_portals(self, map):
        start_x = 0
        start_y = int(len(map) // 2 - len(portal_entrance_left) // 2) #31 // 2 - 7 // 2
        for i in range(len(portal_entrance_left)):
            for j in range(len(portal_entrance_left[0])):
                map[start_y + i][start_x + j] = portal_entrance_left[i][j]
        start_x = len(map[0]) - len(portal_entrance_right[0])
        for i in range(len(portal_entrance_right)):
            for j in range(len(portal_entrance_right[0])):
                map[start_y + i][start_x + j] = portal_entrance_right[i][j]
        return map

    def make_skeleton(self):
        maze = self.generate_thin_maze()
        maze = self.no_dead_ends(maze)
        map = self.convert_to_thick_walls(maze)
        map = self.clear_extra_walls(map)
        map = self.cut_out_14X16_piece(map)
        map = self.add_edges(map)
        map = self.check_connection(map)
        map = self.qudruple_map(map)
        map = self.fill_pockets(map)
        if count_passages_to_walls_ratio(map) > 0.8:
            return map
        else:
            map = self.make_skeleton()
            return map

    def fill_pockets(self, map):
        result = [[0 for j in range(len(map[0]))] for i in range(len(map))]
        stack = []
        start = [15, 0]
        stack.append(start)
        while len(stack) > 0:
            current_cell = stack.pop(0)
            i = current_cell[0]
            j = current_cell[1]
            result[i][j] = 1
            if i < len(map) - 1 and result[i + 1][j] == 0 and map[i + 1][j] == 0:
                stack.append([i + 1, j])
            if i > 0 and result[i - 1][j] == 0 and map[i - 1][j] == 0:
                stack.append([i - 1, j])
            if j < len(map[0]) - 1 and result[i][j + 1] == 0 and map[i][j + 1] == 0:
                stack.append([i, j + 1])
            if j > 0 and result[i][j - 1] == 0 and map[i][j - 1] == 0:
                stack.append([i, j - 1])
        result = inverse(result)
        return result

    def check_connection(self, map):
        for i in range(1, len(map[len(map) - 1]) - 1):
            if map[len(map) - 1][i - 1] == 0 and map[len(map) - 1][i + 1] == 0:
                map[len(map) - 1][i] = 1
        return map

    def add_ghots_house(self, map):
        start_x = int(len(map[0]) / 2 - len(ghosts_house[0]) / 2)  #28 / 2 - 10 / 2
        start_y = int(len(map) // 2 - len(ghosts_house) // 2) #31 // 2 - 7 // 2

        for i in range(len(ghosts_house)):
            for j in range(len(ghosts_house[0])):
                map[start_y + i][start_x + j] = ghosts_house[i][j]
        return map

    def add_edges(self, map):
        for i in range(len(map[0])):
            map[0][i] = 1

        for i in range(len(map)):
            map[i][0] = 1

        return map

    def qudruple_map(self, map):
        original = map
        mirrored_x = copy_2d_array(original)
        for i in range(len(mirrored_x)):
            mirrored_x[i].reverse()
        first_half = []
        for i in range(len(original)):
            line = []
            for j in range(len(original[0])):
                line.append(original[i][j])
            for j in range(len(original[0])):
                line.append(mirrored_x[i][j])
            first_half.append(line)
        second_half = copy_2d_array(first_half)
        second_half.reverse()
        result = []
        for i in range(len(first_half)):
            result.append(first_half[i])
        result.append(middle_separation_line)
        for i in range(len(second_half)):
            result.append(second_half[i])
        return result

    def cut_out_14X16_piece(self, map):
        result = []
        for i in range(1, 16):
            line = []
            for j in range(1, 15):
                line.append(map[i][j])
            result.append(line)
        return result

    def clear_extra_walls(self, map):
        original_ratio = 1
        current_ratio = count_passages_to_walls_ratio(map)
        while current_ratio < original_ratio:
            random_x = random.randint(1, len(map[0]) - 2)
            random_y = random.randint(1, len(map) - 2)
            if map[random_y][random_x] == 1:
                map[random_y][random_x] = 0

            current_ratio = count_passages_to_walls_ratio(map)

        return map

    def convert_to_thick_walls(self, maze):
        result = []
        maze_2d = to_2d(maze, self.width, self.height)

        first_line = [1 for i in range(self.width * 2 + 1)]
        result.append(first_line)

        for i in range(self.height):
            line_up = []
            line_side = []
            line_up.append(1)
            line_side.append(1)
            for j in range(self.width):
                line_side.append(0)
                if maze_2d[i][j].wall_right:
                    line_side.append(1)
                else:
                    line_side.append(0)
            for j in range(self.width - 1):
                if i > 0:
                    if maze_2d[i][j].wall_up:
                        line_up.append(1)
                    else:
                        line_up.append(0)
                    if maze_2d[i][j + 1].wall_up or maze_2d[i][j].wall_right or maze_2d[i - 1][j].wall_right or maze_2d[i][j].wall_up:
                        line_up.append(1)
                    else:
                        line_up.append(0)
            if maze_2d[i][self.width - 1].wall_up:
                line_up.append(1)
            else:
                line_up.append(0)
            line_up.append(1)
            if i > 0:
                result.append(line_up)
            result.append(line_side)

        last_line = [1 for i in range(self.width * 2 + 1)]
        result.append(last_line)
        return result


    def no_dead_ends(self, maze):
        for c in maze:
            if (c.wall_up + c.wall_right + c.wall_down + c.wall_left > 2):
                remove_random_wall(c, maze, self.width, self.height)
        return maze

    def generate_thin_maze(self):
        grid = []
        for i in range(self.height):
            for j in range(self.width):
                new_cell = Cell(i, j, self.width)
                grid.append(new_cell)

        current_cell = grid[0]
        stack = []

        while not is_maze_completed(grid):
            current_cell.visited = True
            next_cell = current_cell.get_next(grid, self.width, self.height)

            if next_cell:
                stack.append(current_cell)
                remove_wall(current_cell, next_cell)
                current_cell = next_cell
            else:
                current_cell = stack.pop()

        return grid


class Cell:
    def __init__(self, i, j, line_len):
        self.i = i
        self.j = j
        self.wall_up = True
        self.wall_down = True
        self.wall_left = True
        self.wall_right = True
        self.visited = False
        self.line_len = line_len

    def get_next(self, grid, width, height):
        neighbors = []

        neighbor_up_index = get_index(self.i - 1, self.j, width, height)
        neighbor_right_index = get_index(self.i, self.j + 1, width, height)
        neighbor_down_index = get_index(self.i + 1, self.j, width, height)
        neighbor_left_index = get_index(self.i, self.j - 1, width, height)

        if neighbor_up_index >= 0:
            if not grid[neighbor_up_index].visited:
                neighbors.append(grid[neighbor_up_index])
        if neighbor_right_index >= 0:
            if not grid[neighbor_right_index].visited:
                neighbors.append(grid[neighbor_right_index])
        if neighbor_down_index >= 0:
            if not grid[neighbor_down_index].visited:
                neighbors.append(grid[neighbor_down_index])
        if neighbor_left_index >= 0:
            if not grid[neighbor_left_index].visited:
                neighbors.append(grid[neighbor_left_index])

        if len(neighbors) > 0:
            rand_index = random.randint(0, len(neighbors) - 1)
            return neighbors[rand_index]
        else:
            return None

def is_maze_completed(grid):
    flag = True
    for c in grid:
        if not c.visited:
            flag = False
    return flag


def get_index(i, j, width, height):
    if i < 0 or i >= height or j < 0 or j >= width:
        return -1 #aka retrun false
    return j + i * width


def remove_wall(cell_a, cell_b):
    shift_x = cell_a.j - cell_b.j
    shift_y = cell_a.i - cell_b.i

    if shift_x == 1:
        cell_a.wall_left = False
        cell_b.wall_right = False
    if shift_x == -1:
        cell_a.wall_right = False
        cell_b.wall_left = False
    if shift_y == 1:
        cell_a.wall_up = False
        cell_b.wall_down = False
    if shift_y == -1:
        cell_a.wall_down = False
        cell_b.wall_up = False


def remove_random_wall(current_cell, grid, width, height):
    walls = []

    neighbor_up_index = get_index(current_cell.i - 1, current_cell.j, width, height)
    neighbor_right_index = get_index(current_cell.i, current_cell.j + 1, width, height)
    neighbor_down_index = get_index(current_cell.i + 1, current_cell.j, width, height)
    neighbor_left_index = get_index(current_cell.i, current_cell.j - 1, width, height)

    if (current_cell.wall_up and neighbor_up_index >= 0):
        walls.append('U')
    if (current_cell.wall_right and neighbor_right_index >= 0):
        walls.append('R')
    if (current_cell.wall_down and neighbor_down_index >= 0):
        walls.append('D')
    if (current_cell.wall_left and neighbor_left_index >= 0):
        walls.append('L')

    random_ind = random.randint(0, len(walls) - 1)
    removeable_wall = walls[random_ind]

    if removeable_wall == 'U':
        current_cell.wall_up = False
        grid[neighbor_up_index].wall_down = False
    if removeable_wall == 'R':
        current_cell.wall_right = False
        grid[neighbor_right_index].wall_left = False
    if removeable_wall == 'D':
        current_cell.wall_down = False
        grid[neighbor_down_index].wall_up = False
    if removeable_wall == 'L':
        current_cell.wall_left = False
        grid[neighbor_left_index].wall_right = False

    return grid


def to_2d(linear_array, width, height):
    result = []
    array_copy = copy_array(linear_array)
    for i in range(height):
        line = []
        for j in range(width):
            line.append(array_copy.pop(0))
        result.append(line)
    return result


def copy_array(array):
    result = []
    for element in array:
        result.append(element)
    return result


def copy_2d_array(array_2d):
    result = []
    for array in array_2d:
        result.append(copy_array(array))
    return result


def count_passages_to_walls_ratio(map):
    walls = 0
    passages = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                walls += 1
            if map[i][j] == 0:
                passages += 1
    ratio = passages / walls
    return ratio


def count_neighbors(map, y, x):
    result = map[y - 1][x] + map[y + 1][x] + map[y][x - 1] + map[y][x + 1]
    return result


def inverse(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                map[i][j] = 0
            elif map[i][j] == 0:
                map[i][j] = 1
    return map


def mirror_change(map, y, x, value):
    map[y][x] = value
    map[y][abs(len(map[0]) - x - 1)] = value
    map[abs(len(map) - y - 1)][x] = value
    map[abs(len(map) - y - 1)][abs(len(map[0]) - x - 1)] = value
    return map


def count_thick_passages(map):
    result = 0
    for i in range(1, len(map) - 2):
        for j in range(1, len(map[i]) - 2):
            if map[i][j] == 0 and map[i + 1][j] == 0 and map[i][j + 1] == 0 and map[i + 1][j + 1] == 0:
                condition_1 = (i >= 11 and i <= 13 and j >= 0 and j <= 4)
                condition_2 = (i >= 17 and i <= 19 and j >= 0 and j <= 4)
                condition_3 = (i >= 11 and i <= 13 and j >= 23 and j <= 27)
                condition_4 = (i >= 17 and i <= 19 and j >= 23 and j <= 27)
                condition_5 = (i >= 14 and i <= 16 and j >= 11 and j <= 16)
                if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:
                    result += 1
    return result

def count_dead_ends(map):
    result = 0
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[i]) - 1):
            neighbors = count_neighbors(map, i, j)
            if neighbors == 3 and map[i][j] == 0:
                result += 1
    return result


def quality_check(map):
    result = True
    if count_passages_to_walls_ratio(map) < 0.8:
        result = False
    if count_thick_passages(map) > 0:
        result = False
    if count_dead_ends(map) > 0:
        result = False
    return result

map_generator = MapGenerator()
