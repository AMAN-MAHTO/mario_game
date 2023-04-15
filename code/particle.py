import pygame
from support import import_images

class ParticleAnimation(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        super().__init__()

        self.frame_index = 0
        self.animation_speed = 0.5
        if type == "jump":
            self.frames = import_images("../graphics/character/dust_particles/jump")
        elif type == "land":
            self.frames = import_images("../graphics/character/dust_particles/land")
        
        self.image = self.frames[self.frame_index]
        self.rect = pos 

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
        
    def update(self,shift):
        
        self.animation()
        self.rect.x -= shift