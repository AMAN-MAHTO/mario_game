import pygame
from sys import exit
from settings import *
from level import Level
from game_data import Level_level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(screen,self.max_level,self.create_level)
        self.staus = "overworld"

        #ui
        self.ui = UI(screen)
        self.health = 100
        self.current_health = 100
        self.coin_count = 0


    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.update_coin_count)
        self.staus = "level"
    
    def create_overworld(self,current_level):
        self.overworld = Overworld(screen,current_level,self.create_level)
        self.staus = 'overworld'
    
    def update_coin_count(self,amount):
        self.coin_count += amount
    
    def run(self):
        if self.staus == "overworld":
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health_bar(self.current_health,self.health)
            self.ui.show_coin(self.coin_count)

pygame.init()
clock = pygame.time.Clock()

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# level_active = False
# current_level=0
# level = Level(level_data = Level_level[current_level],surface = screen)
# overworld = Overworld(screen,current_level)

game = Game()

while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if not level_active:
        #     if events.type == pygame.KEYDOWN:
        #         if events.key == pygame.K_RETURN:
        #             current_level = overworld.level_number
        #             level = Level(level_data = Level_level[current_level],surface = screen)
        #             level_active = True
        # if level_active:
        #     if events.type == pygame.KEYDOWN:
        #         if events.key == pygame.K_ESCAPE:
        #             overworld = Overworld(screen,current_level)
        #             level_active = False


    screen.fill("Black")
    # if level_active:
    #     level.run()
    # else:
    #     overworld.run()

    game.run()


    pygame.display.update()
    clock.tick(60)