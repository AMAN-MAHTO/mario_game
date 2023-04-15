import pygame
from decoration import Sky,Cloud
from settings import *
from random import randint
from support import import_csv_layout
from tiles import StaticTile,AnimatedTile,Tile
from game_data import Level_Passed

class Cursour:
    def __init__(self,surface,center_list,current_level):
        self.display_surface = surface
        self.center_list = center_list
        self.direction = pygame.math.Vector2()
        self.speed = pygame.math.Vector2(5,5)
        self.angled_line_vector = pygame.math.Vector2()

        

        self.current_index = current_level
        self.destination_index = 0
        self.pos = self.center_list[self.current_index]

        self.d_keydown = False
        self.a_keydown = False
        self.level_number = current_level


    def palcing_cursur(self,current_pos,destination_pos):

        #setting speed
        x = destination_pos[0]/100 - current_pos[0]/100
        y = destination_pos[1]/100 - current_pos[1]/100
        self.angled_line_vector.x = x*self.speed.x
        self.angled_line_vector.y = y*self.speed.y


        if self.direction.x <0:
            self.angled_line_vector = -self.angled_line_vector
        

        #moving rect pos
        if self.direction.x > 0:
            self.pos += self.angled_line_vector
            self.destination_reached(self.pos,destination_pos)
        if self.direction.x < 0:
            self.pos -= self.angled_line_vector
            self.destination_reached(self.pos,destination_pos)

        image = pygame.image.load("../graphics/overworld/hat.png")
        
        self.rect = image.get_rect(midbottom = self.pos)
        self.display_surface.blit(image,self.rect)
    
    def destination_reached(self,pos,destination):
        if pos == destination:
            self.direction.x=0
            self.current_index = self.destination_index
            self.pos = self.center_list[self.current_index]
            self.level_number = self.current_index
            
        

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d] and self.d_keydown==False and self.direction.x ==0:
            self.direction.x = 1
            
            self.destination_index += 1
            if self.destination_index > len(self.center_list)-1:
                self.destination_index = len(self.center_list)-1
        
        elif keys[pygame.K_a] and self.a_keydown==False and self.direction.x ==0:
            self.direction.x = -1
            self.destination_index -= 1
            if self.destination_index < 0:
                self.destination_index = 0
       
        # else:
        #     self.direction.x = 0

        self.d_keydown = keys[pygame.K_d]
        self.a_keydown = keys[pygame.K_a]
    
    def update(self):
        self.input()
        self.palcing_cursur(self.center_list[self.current_index],self.center_list[self.destination_index])

        return self.level_number

class Overworld:
    def __init__(self,surface,current_level):
        self.display_surface = surface
        self.world_shift = 0

        #decoration
        self.sky = Sky(7)
        self.cloud = Cloud(SCREEN_HEIGHT-300,SCREEN_WIDTH,20,"../graphics/overworld/clouds")

        #cursour
        
        
        #levels sprites 
        self.level_close_sprties = pygame.sprite.Group()
        self.level_layout = import_csv_layout('../level/overworld/overworld2.csv')
        self.level_open_sprties = self.create_sprites(self.level_layout)
        


        self.center_list = []
        self.center_list_update()

        self.cursour = Cursour(self.display_surface,self.center_list,current_level)
        

    def create_sprites(self,level_layout):
        sprite_group = pygame.sprite.Group()
        for row_index,row_value in enumerate(level_layout):
            for col_index,col_value in enumerate(row_value):
                if col_value != '-1':
                    x = col_index * TILE_SIZE + 100
                    y = row_index * TILE_SIZE + 50
                
                    if col_value == "0":
                        sprite_group.add(AnimatedTile(0,x,y,"../graphics/overworld/0"))
                    if col_value == "1":
                        if Level_Passed[col_value]:
                            sprite_group.add(AnimatedTile(0,x,y,"../graphics/overworld/1"))
                        else:
                            image = pygame.image.load("../graphics/overworld/1/1.png").convert_alpha()
                            image.fill("black",special_flags=pygame.BLEND_RGBA_MULT)
                            self.level_close_sprties.add(StaticTile(0,x,y,image))
                            
                    if col_value == "2":
                        if Level_Passed[col_value]:
                            sprite_group.add(AnimatedTile(0,x,y,"../graphics/overworld/2"))
                        else:
                            image = pygame.image.load("../graphics/overworld/2/1.png").convert_alpha()
                            image.fill("black",special_flags=pygame.BLEND_RGBA_MULT)
                            self.level_close_sprties.add(StaticTile(0,x,y,image))
                        
                    if col_value == "3":
                        if Level_Passed[col_value]:
                            sprite_group.add(AnimatedTile(0,x,y,"../graphics/overworld/3"))
                        else:
                            image = pygame.image.load("../graphics/overworld/3/1.png").convert_alpha()
                            image.fill("black",special_flags=pygame.BLEND_RGBA_MULT)
                            self.level_close_sprties.add(StaticTile(0,x,y,image))
                        
                    if col_value == "4":
                        if Level_Passed[col_value]:
                            sprite_group.add(AnimatedTile(0,x,y,"../graphics/overworld/4"))
                        else:
                            image = pygame.image.load("../graphics/overworld/4/1.png").convert_alpha()
                            image.fill("black",special_flags=pygame.BLEND_RGBA_MULT)
                            self.level_close_sprties.add(StaticTile(0,x,y,image))
                        
                    if col_value == "5":
                        if Level_Passed[col_value]:
                            sprite_group.add(AnimatedTile(0,x,y,"../graphics/overworld/5"))
                        else:
                            image = pygame.image.load("../graphics/overworld/5/1.png").convert_alpha()
                            image.fill("black",special_flags=pygame.BLEND_RGBA_MULT)
                            self.level_close_sprties.add(StaticTile(0,x,y,image))
        
        return sprite_group

    
    def center_list_update(self):
        self.center_list = []
        for sprite in self.level_open_sprties.sprites():
           
           self.center_list.append(sprite.rect.center)
        
        self.center_list.sort(key = lambda x:x[0])

    def run(self):
        self.sky.draw(self.display_surface)
        self.cloud.draw(self.display_surface,0)

        
        self.level_open_sprties.draw(self.display_surface)
        self.level_open_sprties.update(self.world_shift)

        self.level_close_sprties.draw(self.display_surface)

        
        self.level_number = self.cursour.update()

        

        
        
        