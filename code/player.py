import pygame
from settings import *
from support import import_images


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_sprites,good_collision_sprites,surface):
        super().__init__()
        self.diplay_surface = surface
        self.good_collision_sprites = good_collision_sprites       
        
        self.importing_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.18

        self.image = self.animation_dict['idle'][self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)

        #player movement
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = 20

        #player collision
        self.collison_sprites = collision_sprites
        self.on_floor = False
        self.on_celling = False
        self.on_left = False
        self.on_right = False
        self.facing_right = True
        self.current_x = 0

    def earn_pint(self):
        for sprite in self.good_collision_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()

    def importing_player_assets(self):
        current_path = "../graphics/character/"
        self.animation_dict = {"idle": [], 'jump': [], 'run': [], 'fall': []}
        
        for animation in self.animation_dict.keys():
            full_path = current_path + animation
            self.animation_dict[animation] = import_images(full_path)
        
    def animate(self):
        animation_position = self.animation_dict[self.staus]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation_position):
            self.frame_index = 0

        image = animation_position[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set rect
        if self.on_floor and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_floor and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_floor:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_celling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_celling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_celling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def player_status(self):

        if self.direction.y > 1:
            self.staus = "fall"
        if self.direction.y < -1:
            self.staus = 'jump'
        else:
            if self.direction.x != 0:
                self.staus = "run"
            else:
                self.staus = 'idle'

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_w] and self.on_floor:
            self.direction.y = -self.jump_speed

    def horixontal_collision(self):
        for collision_sprites in self.collison_sprites:
            for sprite in collision_sprites.sprites():
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.on_right = True
                        self.current_x = self.rect.right
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.on_left = True
                        self.current_x = self.rect.left

        if self.on_right and (self.current_x < self.rect.right or self.direction.x <= 0):
            self.on_right = False
        if self.on_left and (self.current_x > self.rect.left or self.direction.x >= 0):
            self.on_left = False

    def vertical_collison(self):
        for collision_sprites in self.collison_sprites:
            for sprite in collision_sprites.sprites():
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0
                        self.on_celling = True
                    if self.direction.y > 0:

                        self.rect.bottom = sprite.rect.top

                        self.on_floor = True
                        self.direction.y = 0

        if self.on_floor and self.direction.y > 1 or self.direction.y < 0:
            self.on_floor = False
        if self.on_celling and self.direction.y > 0:
            self.on_celling = False
   
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.input()

        self.rect.x += self.direction.x * self.speed
        self.horixontal_collision()

        self.apply_gravity()
        self.vertical_collison()
        self.player_status()
        self.animate()
        self.earn_pint()
        
        
        
