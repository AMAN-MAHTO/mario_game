from tiles import AnimatedTile
import pygame

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
        

    def update(self,collision_sprites,shift):
        self.collision(collision_sprites)

        self.rect.x += self.direction.x * self.enemy_speed
        if self.direction.x > 0:
            return super().update(shift,flip = True)
        else:
            return super().update(shift)
    
    
