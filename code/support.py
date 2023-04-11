from csv import reader
import pygame
from settings import *
from os import walk

def import_csv_layout(path):
    data_list = []
    with open(path) as map:
        for row in reader(map, delimiter=','):
            data_list.append(list(row))
    return data_list

def import_cut_graphics(path):
    tile_image = pygame.image.load(path).convert_alpha()
    tile_number_x = tile_image.get_size()[0] // TILE_SIZE
    tile_number_y = tile_image.get_size()[1] // TILE_SIZE
    surface_list = []
    for row in range(tile_number_y):
        for col in range(tile_number_x):
            new_surf = pygame.Surface((TILE_SIZE,TILE_SIZE),flags= pygame.SRCALPHA)
            area_rect_x = col * TILE_SIZE
            area_rect_y = row * TILE_SIZE
            new_surf.blit(source = tile_image,dest=(0,0),area=pygame.Rect(area_rect_x,area_rect_y,TILE_SIZE,TILE_SIZE))
            surface_list.append(new_surf)
    return surface_list

def import_graphics(paths):
    surface_list = []
    for path in paths:
        tile_image = pygame.image.load(path).convert_alpha()
        surface_list.append(tile_image)
    return surface_list

def import_images(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            
            full_path = path +'/'+image
            surface_list.append(pygame.image.load(full_path).convert_alpha())
    
    return surface_list