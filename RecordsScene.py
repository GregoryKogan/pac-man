import pygame
from Variables import *
from DB_communicator import *


class RecordsScene:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.stay_here = True

    def update(self, user_input):
        self.manage_user_input(user_input)

        font_regular = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 50)
        font_large = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 70)
        font_small = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 30)
        lines = get_all()
        lines.reverse()

        surfaces = []
        for line in lines:
            new_surface = font_regular.render(line, True, color_white)
            surfaces.append(new_surface)

        header = font_large.render("RECORDS", True, color_white)
        go_back_text = font_small.render("Press 'B' to go back", True, color_white)
        middle = self.screen.get_width() // 2
        self.screen.fill(color_black)
        self.screen.blit(header, (middle - header.get_width() // 2, 20))
        self.screen.blit(go_back_text, (middle - header.get_width() // 2, self.screen.get_height() - 50))

        for i in range(len(surfaces)):
            self.screen.blit(surfaces[i], (100, 100 + 40 * i))

    def manage_user_input(self, user_input):
        if user_input[pygame.K_b]:
            self.stay_here = False
