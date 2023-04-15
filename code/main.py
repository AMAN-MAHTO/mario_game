import pygame
from sys import exit
from settings import *
from level import Level
from game_data import level_0,level_2
from overworld import Overworld

pygame.init()
clock = pygame.time.Clock()

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

level = Level(level_data = level_2,surface = screen)

level_active = False

overworld = Overworld(screen)

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not level_active:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    level_active = True


    screen.fill("Black")
    if level_active:
        level.run()
    else:
        overworld.run()


    pygame.display.update()
    clock.tick(60)