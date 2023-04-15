import pygame
from decoration import Sky,Cloud
from settings import *
from random import randint

class Cursour:
    def __init__(self,surface,center_list):
        self.display_surface = surface
        self.center_list = center_list
        self.direction = pygame.math.Vector2()
        self.cursur_speed = pygame.math.Vector2(5,5)

        self.current_index = 0
        self.destination_index = 0
        self.pos = center_list[self.current_index]

        self.d_keydown = False
        self.a_keydown = False


    def palcing_cursur(self,current_pos,destination_pos):

        #setting speed
        x = destination_pos[0]/100 - current_pos[0]/100
        y = destination_pos[1]/100 - current_pos[1]/100
        angled_line_vector = pygame.math.Vector2(x,y)
        if self.direction.x <0:
            angled_line_vector = -angled_line_vector
        

        #moving rect pos
        if self.direction.x > 0:
            self.pos += angled_line_vector
            self.destination_reached(self.pos,destination_pos)
        if self.direction.x < 0:
            self.pos -= angled_line_vector
            self.destination_reached(self.pos,destination_pos)

        image = pygame.Surface((30,30))
        image.fill("blue")
        rect = image.get_rect(center = self.pos)
        self.display_surface.blit(image,rect)
    
    def destination_reached(self,pos,destination):
        if pos == destination:
            self.direction.x=0
            self.current_index = self.destination_index
            self.pos = self.center_list[self.current_index]
        

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

class Overworld:
    def __init__(self,surface):
        self.display_surface = surface

        self.sky = Sky(7)
        self.cloud = Cloud(SCREEN_HEIGHT-300,SCREEN_WIDTH,20,"../graphics/overworld/clouds")
        self.layout()
        self.cursour = Cursour(self.display_surface,self.center_list)
        
    
    
    def layout(self):
        rect_list = [(100,500),(300,100),(500,400),(700,50),(900,600)]
        self.center_list =[]
        for i in range(5):
            image = pygame.Surface((100,100))
            image.fill("red")
            rect = image.get_rect(topleft = rect_list[i])
            self.display_surface.blit(image,rect)
            self.center_list.append(rect.center)
        
        

    def run(self):
        self.sky.draw(self.display_surface)
        self.cloud.draw(self.display_surface,0)
        self.layout()
        self.cursour.update()
        
        
        