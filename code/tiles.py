import pygame
from support import import_images
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()

        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self):
        self.rect.x -= 1
        

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class Crate(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface
        
        offset_x = x + TILE_SIZE - self.image.get_size()[0]
        offset_y = y + TILE_SIZE - self.image.get_size()[1]
        self.rect = self.image.get_rect(topleft = (offset_x,offset_y))

class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        
        self.frames = import_images(path)
        
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.frames[self.frame_index]
        self.image.get_rect(topleft = (x,y))
        self.set_rect()
        

    def set_rect(self):
        offset_x = self.rect.x + TILE_SIZE - self.image.get_size()[0]
        offset_y = self.rect.y + TILE_SIZE - self.image.get_size()[1]
        self.rect = self.image.get_rect(topleft = (offset_x,offset_y))
    
    def update_frame(self,flip):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        if flip:
            image = self.frames[int(self.frame_index)]
            flip_image = pygame.transform.flip(image,True,False)
            self.image = flip_image
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update(self,flip= False):
        self.update_frame(flip)
       
        return super().update()

class Enemy(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.direction = pygame.math.Vector2(-1,0)
        self.enemy_speed = 2
    def collision(self,collision_sprites):
        for sprtie in collision_sprites:
            if sprtie.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprtie.rect.right 
                    self.direction.x = 1
                elif self.direction.x > 0:
                    self.rect.right = sprtie.rect.left 
                    self.direction.x = -1
        

    def update(self,collision_sprites):
        self.collision(collision_sprites)

        self.rect.x += self.direction.x * self.enemy_speed
        if self.direction.x > 0:
            return super().update(flip = True)
        else:
            return super().update()