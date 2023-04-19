import pygame
from sys import exit
from settings import *
from level import Level
from game_data import Level_level,Level_Passed
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(screen,self.max_level,self.create_level,self.create_no_level_message)
        self.staus = "overworld"

        #ui
        self.ui = UI(screen)
        self.health = 100
        self.current_health = 100
        self.coin_count = 0

    def create_no_level_message(self):
        self.ui.show_no_level_message()

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.update_coin_count,self.update_health,self.what_current_health,self.reset)
        self.staus = "level"

    
    def create_overworld(self,current_level):
        self.overworld = Overworld(screen,current_level,self.create_level,self.create_no_level_message)
        self.staus = 'overworld'
    
    def what_current_health(self):
        return self.current_health

    def update_coin_count(self,amount):
        self.coin_count += amount

    def update_health(self,amount):
        self.current_health += amount
    
    def reset(self):
        self.current_health = 100
        self.coin_count = 0
        for key in Level_Passed.keys():
            if key != '0':
                Level_Passed[key] = False
                
        current_level = 0
        self.create_overworld(0)

    def run(self):
        if self.staus == "overworld":
            self.overworld.run()
            overworld_music.play(loops= -1)
            level_music.stop()
        elif self.staus == 'level':
            self.level.run()
            self.ui.show_health_bar(self.current_health,self.health)
            self.ui.show_coin(self.coin_count)
            overworld_music.stop()
            # level_music.play(loops= -1)
        
        
        if self.current_health <=0:
            pygame.time.wait(1000)
            self.reset()

pygame.init()
clock = pygame.time.Clock()

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#sound
overworld_music = pygame.mixer.Sound('../audio/overworld_music.wav')

level_music = pygame.mixer.Sound("../audio/level_music.wav")


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