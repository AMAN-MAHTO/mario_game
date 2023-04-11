import pygame
from sys import exit
from settings import *
from level import Level
from game_data import level_0
pygame.init()
clock = pygame.time.Clock()

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

level = Level(level_data = level_0,surface = screen)

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill("Black")
    level.run()
    pygame.display.update()
    clock.tick(60)