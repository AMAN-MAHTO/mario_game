import pygame
from sys import exit
from settings import *
from level import Level
from game_data import Level_level
from overworld import Overworld

pygame.init()
clock = pygame.time.Clock()

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))



level_active = False
current_level=0
overworld = Overworld(screen,current_level)

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not level_active:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_RETURN:
                    current_level = overworld.level_number
                    level = Level(level_data = Level_level[current_level],surface = screen)
                    level_active = True
        if level_active:
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    overworld = Overworld(screen,current_level)
                    level_active = False


    screen.fill("Black")
    if level_active:
        level.run()
    else:
        overworld.run()


    pygame.display.update()
    clock.tick(60)