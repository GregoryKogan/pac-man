import pygame
import random
from Variables import *


class Ghost:
    def __init__(self, name, screen_width, map, position, cell_width):
        self.screen = pygame.Surface((screen_width, screen_width), pygame.SRCALPHA)
        self.map = map
        self.direction_movement = 'U'
        self.speed = 1.88
        self.pos_x = position[1] #j - index
        self.pos_y = position[0] #i - index
        self.cell_width = cell_width
        self.screen_pos_x = cell_width * self.pos_x - cell_width // 4
        self.screen_pos_y = cell_width * self.pos_y - cell_width // 4
        self.name = name
        self.mode = "Normal"
        self.target = None
        self.timer = 0
        self.last_cell = [self.pos_y, self.pos_x]
        if self.name == "Blinky":
            self.color = color_red
        elif self.name == "Inky":
            self.color = color_inky
        elif self.name == "Pinky":
            self.color = color_pink
        elif self.name == "Clyde":
            self.color = color_clyde
        else:
            self.color = color_white

    def update(self, pacman, blinky=None):
        self.timer += 1

        if self.mode == "Scared" and self.timer > 850:
            self.mode = "Normal"

        target = self.get_target(pacman, blinky)
        self.target = target
        self.follow_target(target)
        self.manage_speed([pacman.pos_x, pacman.pos_y])
        self.manage_position()

        self.screen.fill(color_transparent)
        sprite_path = None
        if self.mode == "Normal":
            sprite_path = "Static/Sprites/" + str(self.name) + "/" + str(self.name) + "-" + self.direction_movement + ".png"
        else:
            sprite_faze = str((self.timer % 30 > 15) + 1)
            sprite_path = "Static/Sprites/Scared/Fear-" + sprite_faze + ".png"
        sprite = pygame.image.load(sprite_path)
        self.screen.blit(sprite, (0, 0))

    def get_target(self, pacman, blinky=None):
        if self.mode == "Scared":
            if self.timer % 20 == 1:
                return [random.randint(0, 30), random.randint(0, 27)]
            else:
                return self.target

        if self.map[self.pos_y][self.pos_x] == 'U':
            return [13, 0]

        if self.name == "Blinky":
            return [pacman.pos_x, pacman.pos_y]
        if self.name == "Pinky":
            pacman_direction = pacman.direction_movement
            target_x = None
            target_y = None
            if pacman_direction == 'U':
                target_x = pacman.pos_x
                target_y = pacman.pos_y - 4
            if pacman_direction == 'R':
                target_x = pacman.pos_x + 4
                target_y = pacman.pos_y
            if pacman_direction == 'D':
                target_x = pacman.pos_x
                target_y = pacman.pos_y + 4
            if pacman_direction == 'L':
                target_x = pacman.pos_x - 4
                target_y = pacman.pos_y
            return [target_x, target_y]
        if self.name == "Inky":
            vector_x = blinky.pos_x - pacman.pos_x
            target_x = pacman.pos_x - vector_x
            vector_y = blinky.pos_y - pacman.pos_y
            target_y = pacman.pos_y - vector_y
            return [target_x, target_y]
        if self.name == "Clyde":
            dist_to_pacman = dist(pacman.pos_x, pacman.pos_y, self.pos_x, self.pos_y)
            if dist_to_pacman <= 8:
                return [14, 15]
            else:
                return [pacman.pos_x, pacman.pos_y]

    def follow_target(self, target):
        self.update_pos()
        i = self.pos_y
        j = self.pos_x

        potential_directions = []
        if self.direction_movement != 'U':
            potential_directions.append('D')
        if self.direction_movement != 'R':
            potential_directions.append('L')
        if self.direction_movement != 'D':
            potential_directions.append('U')
        if self.direction_movement != 'L':
            potential_directions.append('R')

        final_directions = []
        last_i = self.last_cell[0]
        last_j = self.last_cell[1]
        for direction in potential_directions:
            if direction == 'U' and self.map[i - 1][j] == 'O':
                if last_i != i - 1 or last_j != j:
                    final_directions.append('U')
            if direction == 'R' and self.map[i][j + 1] == 'O':
                if last_i != i or last_j != j + 1:
                    final_directions.append('R')
            if direction == 'D' and self.map[i + 1][j] == 'O':
                if last_i != i + 1 or last_j != j:
                    final_directions.append('D')
            if direction == 'L' and self.map[i][j - 1] == 'O':
                if last_i != i or last_j != j - 1:
                    final_directions.append('L')

        if len(final_directions) == 0:
            for direction in potential_directions:
                if direction == 'U' and self.map[i - 1][j] != '#':
                    if last_i != i - 1 or last_j != j:
                        final_directions.append('U')
                if direction == 'R' and self.map[i][j + 1] != '#':
                    if last_i != i or last_j != j + 1:
                        final_directions.append('R')
                if direction == 'D' and self.map[i + 1][j] != '#':
                    if last_i != i + 1 or last_j != j:
                        final_directions.append('D')
                if direction == 'L' and self.map[i][j - 1] != '#':
                    if last_i != i or last_j != j - 1:
                        final_directions.append('L')


        direction_desired = None
        shortest_dist = 1000
        for direction in final_directions:
            if direction == 'U':
                if dist(target[0], target[1], j, i - 1) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j, i - 1)
                    direction_desired = 'U'
            if direction == 'R':
                if dist(target[0], target[1], j + 1, i) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j + 1, i)
                    direction_desired = 'R'
            if direction == 'D':
                if dist(target[0], target[1], j, i + 1) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j, i + 1)
                    direction_desired = 'D'
            if direction == 'L':
                if dist(target[0], target[1], j - 1, i) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j - 1, i)
                    direction_desired = 'L'

        if direction_desired:
            self.direction_movement = direction_desired

    def manage_speed(self, target):
        if self.pos_x == target[0] and self.pos_y == target[1]:
            self.speed = 0
        else:
            if self.mode == "Normal":
                self.speed = 1.88
            else:
                self.speed = 1.5

    def manage_position(self):
        if self.direction_movement == 'U':
            self.screen_pos_y -= self.speed
        if self.direction_movement == 'R':
            self.screen_pos_x += self.speed
        if self.direction_movement == 'D':
            self.screen_pos_y += self.speed
        if self.direction_movement == 'L':
            self.screen_pos_x -= self.speed
        self.align()

    def align(self):
        if self.direction_movement == 'U' or self.direction_movement == 'D':
            self.align_horizontal()
        if self.direction_movement == 'R' or self.direction_movement == 'L':
            self.align_vertical()

    def align_vertical(self):
        self.screen_pos_y = self.cell_width * self.pos_y - self.cell_width // 4

    def align_horizontal(self):
        self.screen_pos_x = self.cell_width * self.pos_x - self.cell_width // 4

    def update_pos(self):
        new_pos_x = int((self.screen_pos_x + (self.screen.get_width() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)
        new_pos_y = int((self.screen_pos_y + (self.screen.get_height() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)
        if new_pos_x != self.pos_x or new_pos_y != self.pos_y:
            self.last_cell = [self.pos_y, self.pos_x]
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y

    def go_to_scare_mode(self):
        self.mode = "Scared"
        self.timer = 0


def dist(x1, y1, x2, y2):
    return (abs(x1 - x2)**2 + abs(y1 - y2)**2)**0.5
