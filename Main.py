import pygame
from Application import *


pygame.init()
main_screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pac-Man - G.Koganovskiy")
pygame.display.set_icon(pygame.image.load("Static/Sprites/Pacman/Pacman-Open-R.png"))
frame_rate = pygame.time.Clock()

game_application = Application()

running = True
while running:
    running = stop_check()
    main_screen.fill((18, 18, 18))
    frame_rate.tick(60)
    game_application.update(pygame.key.get_pressed())
    main_screen.blit(game_application.screen, (0, 0))
    pygame.display.update()

pygame.QUIT
