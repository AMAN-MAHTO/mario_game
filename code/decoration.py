from settings import *
import pygame
from support import import_images
from tiles import AnimatedTile,StaticTile
from random import randint,choice

class Sky:
    def __init__(self,horizon):
        sky_tiles = import_images("../graphics/decoration/sky")
        self.sky_top = pygame.transform.scale(sky_tiles[2],(SCREEN_WIDTH,TILE_SIZE))
        self.sky_mid = pygame.transform.scale(sky_tiles[1],(SCREEN_WIDTH,TILE_SIZE))
        self.sky_bottom = pygame.transform.scale(sky_tiles[0],(SCREEN_WIDTH,TILE_SIZE))
        self.horizon = horizon

    def draw(self,surface):
        for row in range(vertical_tile_number):
            if row < self.horizon:
                surface.blit(self.sky_top,(0,row*TILE_SIZE))
            elif row == self.horizon:
                surface.blit(self.sky_mid,(0,row*TILE_SIZE))
            else:
                surface.blit(self.sky_bottom,(0,row*TILE_SIZE))

class Water:
    def __init__(self,top,level_length):
        self.water_sprite = pygame.sprite.Group()
        sart_x = -SCREEN_WIDTH
        water_tile_width = 192
        number_of_water_tile_x = int((level_length + SCREEN_WIDTH) / water_tile_width) + 70
        
        y = top 
        for val in range(number_of_water_tile_x):
            sprite = AnimatedTile(192,val*TILE_SIZE + sart_x,y,"../graphics/decoration/water")
            self.water_sprite.add(sprite)
        
    def draw(self,surface,shift):
        self.water_sprite.update(shift)
        self.water_sprite.draw(surface)

class Cloud:
    def __init__(self,horizon,level_length,number_of_cloud,image_folder_path = '../graphics/decoration/clouds'):
        min_x = -SCREEN_WIDTH
        max_x = level_length +SCREEN_WIDTH
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for i in range(number_of_cloud):
            cloud = choice(import_images(image_folder_path))
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            self.cloud_sprites.add(StaticTile(0,x,y,cloud))

    def draw(self,surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)

        