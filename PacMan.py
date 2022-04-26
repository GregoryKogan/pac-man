import pygame
from Variables import *


class PacMan:
    def __init__(self, screen_width, map, position, cell_width):
        self.screen = pygame.Surface((screen_width, screen_width), pygame.SRCALPHA)
        self.map = map
        self.direction_movement = 'R'
        self.direction_desired = 'R'
        self.speed = 2
        self.pos_x = position[1] #j - index
        self.pos_y = position[0] #i - index
        self.cell_width = cell_width
        self.screen_pos_x = cell_width * self.pos_x - cell_width // 4
        self.screen_pos_y = cell_width * self.pos_y - cell_width // 4
        self.sprite_faze = 0

    def update(self, user_input):
        self.manage_portals()
        self.manage_user_input(user_input)
        self.manage_speed()
        self.manage_position()
        self.screen.fill(color_transparent)
        sprite_path = f"Static/Sprites/Pacman/Pacman-{self.get_sprite()}"
        sprite = pygame.image.load(sprite_path)
        self.screen.blit(sprite, (0, 0))
        # pygame.draw.circle(self.screen, color_yellow, (self.screen.get_width() // 2, self.screen.get_height() // 2), self.screen.get_width() // 2)

    def get_sprite(self):
        self.sprite_faze += 0.35
        if self.sprite_faze > 3:
            self.sprite_faze = 0
        fazes = ["Closed", "Ajar", "Open", "Ajar"]

        if fazes[int(self.sprite_faze)] != "Closed":
            return f"{fazes[int(self.sprite_faze)]}-{self.direction_movement}.png"
        else:
            return f"{fazes[int(self.sprite_faze)]}.png"

    def manage_portals(self):
        self.update_pos()
        portal_pos = find_portals(self.map)
        p1_pos = [portal_pos[0], portal_pos[1]]
        p2_pos = [portal_pos[2], portal_pos[3]]
        if self.map[self.pos_y][self.pos_x] == 'p1':
            self.pos_x = p2_pos[1] - 1
            self.pos_y = p2_pos[0]
            self.screen_pos_x = self.cell_width * self.pos_x - self.cell_width // 4
            self.screen_pos_y = self.cell_width * self.pos_y - self.cell_width // 4
        if self.map[self.pos_y][self.pos_x] == 'p2':
            self.pos_x = p1_pos[1] + 1
            self.pos_y = p1_pos[0]
            self.screen_pos_x = self.cell_width * self.pos_x - self.cell_width // 4
            self.screen_pos_y = self.cell_width * self.pos_y - self.cell_width // 4

    def manage_position(self):
        if self.direction_movement == 'D':
            self.screen_pos_y += self.speed
        elif self.direction_movement == 'L':
            self.screen_pos_x -= self.speed
        elif self.direction_movement == 'R':
            self.screen_pos_x += self.speed
        elif self.direction_movement == 'U':
            self.screen_pos_y -= self.speed
        self.align()

    def manage_speed(self):
        i = self.pos_y
        j = self.pos_x
        if self.direction_movement == 'D':
            if self.map[i + 1][j] != '#':
                self.speed = 2
            elif self.screen_pos_y > self.pos_y * self.cell_width - self.cell_width // 4:
                self.screen_pos_y = self.pos_y * self.cell_width - self.cell_width // 4
                self.speed = 0
        elif self.direction_movement == 'L':
            if self.map[i][j - 1] != '#':
                self.speed = 2
            elif self.screen_pos_x < self.pos_x * self.cell_width - self.cell_width // 4:
                self.screen_pos_x = self.pos_x * self.cell_width - self.cell_width // 4
                self.speed = 0

        elif self.direction_movement == 'R':
            if self.map[i][j + 1] != '#':
                self.speed = 2
            elif self.screen_pos_x > self.pos_x * self.cell_width - self.cell_width // 4:
                self.screen_pos_x = self.pos_x * self.cell_width - self.cell_width // 4
                self.speed = 0
        elif self.direction_movement == 'U':
            if self.map[i - 1][j] != '#':
                self.speed = 2
            elif self.screen_pos_y < self.pos_y * self.cell_width - self.cell_width // 4:
                self.screen_pos_y = self.pos_y * self.cell_width - self.cell_width // 4
                self.speed = 0

    def manage_user_input(self, user_input):
        self.update_pos()
        i = self.pos_y
        j = self.pos_x

        if user_input[pygame.K_w]:
            self.direction_desired = 'U'
        if user_input[pygame.K_d]:
            self.direction_desired = 'R'
        if user_input[pygame.K_s]:
            self.direction_desired = 'D'
        if user_input[pygame.K_a]:
            self.direction_desired = 'L'

        if self.direction_desired == 'U' and self.map[i - 1][j] != '#':
            self.direction_movement = self.direction_desired
        if self.direction_desired == 'R' and self.map[i][j + 1] != '#':
            self.direction_movement = self.direction_desired
        if self.direction_desired == 'D' and self.map[i + 1][j] != '#':
            self.direction_movement = self.direction_desired
        if self.direction_desired == 'L' and self.map[i][j - 1] != '#':
            self.direction_movement = self.direction_desired

    def align(self):
        if self.direction_movement in ['U', 'D']:
            self.align_horizontal()
        if self.direction_movement in ['R', 'L']:
            self.align_vertical()

    def align_vertical(self):
        self.screen_pos_y = self.cell_width * self.pos_y - self.cell_width // 4

    def align_horizontal(self):
        self.screen_pos_x = self.cell_width * self.pos_x - self.cell_width // 4

    def update_pos(self):
        self.pos_x = int((self.screen_pos_x + (self.screen.get_width() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)
        self.pos_y = int((self.screen_pos_y + (self.screen.get_height() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)


def find_portals(map):
    result = [None] * 4
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'p1':
                result[0] = i
                result[1] = j
            if map[i][j] == 'p2':
                result[2] = i
                result[3] = j
    return result
