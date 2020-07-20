import pygame
from GameScene import *
from LogInScene import *
from RecordsScene import *


class Application:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.current_scene = "Login"
        self.scene_game = GameScene()
        self.scene_records = RecordsScene()
        self.scene_login = LogInScene()

        self.username = None

        pygame.mixer.music.load('Static/Sounds/background.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def update(self, user_input):
        self.logic(user_input)

        if self.current_scene == "Game":
            self.scene_game.update(user_input)
            self.screen.blit(self.scene_game.screen, (0, 0))
        if self.current_scene == "Login":
            self.scene_login.update()
            self.screen.blit(self.scene_login.screen, (0, 0))
        if self.current_scene == "Records":
            self.scene_records.update(user_input)
            self.screen.blit(self.scene_records.screen, (0, 0))


    def logic(self, user_input):
        if self.scene_login.done and self.current_scene == "Login":
            self.username = self.scene_login.nickname
            self.scene_game.username = self.username
            self.scene_game.setup("generated")
            pygame.mixer.music.set_volume(0.1)
            self.current_scene = "Game"
        if self.scene_game.stay_here == False and self.current_scene == "Game":
            self.scene_game.stay_here = True
            pygame.mixer.music.set_volume(0.5)
            self.current_scene = "Records"
        if self.scene_records.stay_here == False and self.current_scene == "Records":
            self.scene_records.stay_here = True
            pygame.mixer.music.set_volume(0.1)
            self.current_scene = "Game"


def stop_check():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    user_input = pygame.key.get_pressed()
    if user_input[pygame.K_ESCAPE]:
        return False
    return True
