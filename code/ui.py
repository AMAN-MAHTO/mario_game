import pygame
from settings import SCREEN_HEIGHT,SCREEN_WIDTH

class UI:
    def __init__(self,screen):
        self.diaplay_surface = screen

        self.health_bar = pygame.image.load("../graphics/ui/health_bar.png")
        self.health_bar_topleft = (53,39)
        self.bar_max_width = 154
        self.bar_height = 4

        self.coin = pygame.image.load("../graphics/ui/coin.png")
        self.coin_rect = self.coin.get_rect(topleft = (50,60))

        self.font = pygame.font.Font("../graphics/ui/ARCADEPI.TTF",25)


    def show_health_bar(self,current,full):
        self.diaplay_surface.blit(self.health_bar,(20,10))
        bar_ratio = self.bar_max_width / full  
        bar_width = current * bar_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft,(bar_width,self.bar_height))
        pygame.draw.rect(self.diaplay_surface,'#D30000',health_bar_rect)



    def show_coin(self,amount):
        text_surface = self.font.render(f"{amount}",False,'#33323d')
        text_rect = text_surface.get_rect(midleft = (self.coin_rect.right + 10,self.coin_rect.centery))
        self.diaplay_surface.blit(self.coin,self.coin_rect)
        self.diaplay_surface.blit(text_surface,text_rect)
    
    def show_no_level_message(self):
        
        text_surface = self.font.render("Comming soon!",False,'#33323d')
        text_rect = text_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.diaplay_surface.blit(text_surface,text_rect)
        
        