import pygame
from Variables import *


class LogInScene:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.nickname = ""
        self.done = False
        self.font_header = pygame.font.Font('Static/Fonts/PAC-FONT.ttf', 120)
        self.font_sub_header = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 60)
        self.font_regular = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 50)
        self.font_small = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 30)
        self.render()

    def update(self):
        events = pygame.event.get()
        while not self.done and len(events) > 0:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.nickname = self.nickname[:-1]
                    else:
                        if len(self.nickname) < 15:
                            self.nickname += event.unicode
            events = pygame.event.get()
        self.render()

    def render(self):
        self.screen.fill(color_black)
        header_text = self.font_header.render("Pac----Man", True, color_white)
        sub_header_text = self.font_sub_header.render("Enter your nickname", True, color_white)
        nickname_text = self.font_regular.render(self.nickname, True, color_white)
        enter_text = self.font_small.render("Press 'Enter' to submit", True, color_white)
        middle = self.screen.get_width() // 2
        self.screen.blit(header_text, (middle - header_text.get_width() // 2, 30))
        self.screen.blit(sub_header_text, (middle - sub_header_text.get_width() // 2, 250))
        self.screen.blit(nickname_text, (middle - nickname_text.get_width() // 2, 350))
        pygame.draw.rect(self.screen, color_white, (middle - nickname_text.get_width() // 2 - 10, 360 - 10, nickname_text.get_width() + 15, nickname_text.get_height()), 3)
        if len(self.nickname) > 0:
            self.screen.blit(enter_text, (middle - enter_text.get_width() // 2, 440))
