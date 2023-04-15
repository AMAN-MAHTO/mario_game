import pygame
from settings import *
from support import import_csv_layout,import_cut_graphics,import_graphics
from tiles import Tile,StaticTile,Crate,AnimatedTile
from enemy import Enemy
from decoration import Sky,Cloud,Water
from player import Player
from particle import ParticleAnimation


class Level:
    def __init__(self,level_data,surface):
        self.world_shift = 0
        self.display_surface = surface
        self.tarrain_layout = import_csv_layout(level_data['terrain'])
        self.tarrain_sprites = self.create_tile_group(self.tarrain_layout,'tarrain')

        self.grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(self.grass_layout,type='grass')

        self.crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(self.crates_layout,'crates')

        self.fb_palms_layout = import_csv_layout(level_data['fb_palms'])
        self.fb_palms_sprites = self.create_tile_group(self.fb_palms_layout,'fb_palms')

        self.bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(self.bg_palms_layout,'bg_palms')

        self.coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(self.coins_layout,'coins')

        self.enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(self.enemies_layout,'enemies')
        self.enemies_obstacle_sprites = self.create_tile_group(self.enemies_layout,'enemies_obstacle')

        #player
        self.goal_sprite = pygame.sprite.GroupSingle()
        self.player_sprites = pygame.sprite.GroupSingle()
        self.player_layout = import_csv_layout(level_data['player'])
        self.player_setup(self.player_layout)
        

        #decoration
        self.sky = Sky(8)
        level_length = len(self.tarrain_layout[0]) * TILE_SIZE
        self.water_sprite = Water(SCREEN_HEIGHT - 30,level_length)
        self.cloud_sprites = Cloud(SCREEN_HEIGHT - 400,level_length,30)


        #run particle animation
        self.particle_frame_index = 0
        self.particle_animation_speed = 0.15

        #jump particle animation
        self.jump_sprtie = pygame.sprite.GroupSingle()


    def create_tile_group(self,levle_layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row_value in enumerate(levle_layout):
            for col_index,col_value in enumerate(row_value):
                if col_value != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == "tarrain":
                        tarrain_tiles= import_cut_graphics(TILE_IMAGE_PATH["tarrain"])
                        tarrain_tile_surface = tarrain_tiles[int(col_value)]
                        tile_sprite = StaticTile(TILE_SIZE,x,y,tarrain_tile_surface)
                        sprite_group.add(tile_sprite)

                    if type == 'grass':
                        grass_tiles= import_cut_graphics(TILE_IMAGE_PATH['grass'])
                        grass_tile_surface = grass_tiles[int(col_value)]
                        tile_sprite = StaticTile(TILE_SIZE,x,y,grass_tile_surface)
                        sprite_group.add(tile_sprite)
                    
                    if type == "crates":
                        crates_tiles = import_graphics(TILE_IMAGE_PATH["crates"])
                        crates_tile_surface = crates_tiles[int(col_value)] 
                        tile_sprite = Crate(TILE_SIZE,x,y,crates_tile_surface)
                        sprite_group.add(tile_sprite)
                    
                    if type == "fb_palms":
                        if col_value == "1":
                            path = '../graphics/terrain/palm_large'
                        else:
                            path = '../graphics/terrain/palm_small'
                        tile_sprite = AnimatedTile(TILE_SIZE,x,y,path)
                        sprite_group.add(tile_sprite)
                    
                    if type == "bg_palms":
                        
                        path = '../graphics/terrain/palm_bg'
                        
                        tile_sprite = AnimatedTile(TILE_SIZE,x+30,y,path)
                        sprite_group.add(tile_sprite)
                    
                    if type == "coins":
                        if col_value == "0":
                            path = "../graphics/coins/gold"
                        else:
                            path = "../graphics/coins/silver"
                         
                        tile_sprite = AnimatedTile(TILE_SIZE,x,y,path)
                        sprite_group.add(tile_sprite)
                    
                    if type == "enemies":
                        if col_value == "0":
                            path = "../graphics/enemy/run"
                            tile_sprite = Enemy(TILE_SIZE,x,y,path)
                            sprite_group.add(tile_sprite)
                    if type == "enemies_obstacle":
                        if col_value == "1":
                            tile_sprite = Tile(TILE_SIZE,x,y)
                            sprite_group.add(tile_sprite)
                    

                    

        return sprite_group
    
    def run_particle_animation(self):
        player = self.player_sprites.sprite
        if player.staus == 'run' and player.on_floor:
            run_frame_list = player.particle_dict['run']
            self.particle_frame_index += self.particle_animation_speed
            if self.particle_frame_index >= len(run_frame_list): self.particle_frame_index = 0
            image = run_frame_list[int(self.particle_frame_index)]
            if player.facing_right:
                pos = player.rect.bottomleft + pygame.math.Vector2(-8,-10)
            
            else:
                pos = player.rect.bottomright + pygame.math.Vector2(0,-10)
                image = pygame.transform.flip(image,True,False)
            
        
            self.display_surface.blit(image,pos)
    
    def create_jump_particle(self):
        player = self.player_sprites.sprite
        if player.facing_right:
            offset = player.rect.midbottom - pygame.math.Vector2(28,30)
            self.jump_sprtie.add(ParticleAnimation(offset,'jump'))
        else:
            offset = player.rect.midbottom - pygame.math.Vector2(2,30)
            self.jump_sprtie.add(ParticleAnimation(offset,'jump'))
    
    def create_landing_particle(self):
        player = self.player_sprites.sprite
        if self.on_ground_before_verticle_collision == False and player.on_floor:
            if player.facing_right:
                offset = player.rect.midbottom - pygame.math.Vector2(65,40)
                self.jump_sprtie.add(ParticleAnimation(offset,'land'))
            else:
                offset = player.rect.midbottom - pygame.math.Vector2(35,40)
                self.jump_sprtie.add(ParticleAnimation(offset,'land'))
    

    def player_setup(self,layout):
        
        for row_index,row_val in enumerate(layout):
            for col_index,col_value in enumerate(row_val):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col_value != '-1':
                    if col_value == '0':
                        collidabel_sprites = [self.tarrain_sprites,self.crates_sprites]
                        good_collidabel_sprites = self.coins_sprites
                        sprite = Player((x,y),collidabel_sprites,good_collidabel_sprites,self.display_surface)
                        self.player_sprites.add(sprite)
                    else:
                        hat_image = pygame.image.load('../graphics/character/hat.png')
                        sprite = StaticTile(TILE_SIZE,x,y,hat_image)
                        self.goal_sprite.add(sprite)
    
    def scroll_x(self):
        player = self.player_sprites.sprite
        player_x = player.rect.centerx

        if player_x < SCREEN_WIDTH /4 and player.direction.x < 0:
            self.world_shift = -8
            player.speed = 0
        elif player_x > SCREEN_WIDTH -(SCREEN_WIDTH /4) and player.direction.x > 0:
            self.world_shift = 8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horixontal_collision(self):
        player = self.player_sprites.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tarrain_sprites.sprites() + self.crates_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.on_right = True
                    player.current_x = player.rect.right
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    player.current_x = player.rect.left

        if player.on_right and (player.current_x < player.rect.right or player.direction.x <= 0):
            player.on_right = False
        if player.on_left and (player.current_x > player.rect.left or player.direction.x >= 0):
            player.on_left = False

    def vertical_collison(self):
        player = self.player_sprites.sprite
        player.apply_gravity()

        
        for sprite in self.tarrain_sprites.sprites() + self.crates_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_celling = True
                if player.direction.y > 0:

                    player.rect.bottom = sprite.rect.top

                    player.on_floor = True
                    player.direction.y = 0

        if player.on_floor and player.direction.y > 1 or player.direction.y < 0:
            player.on_floor = False
        if player.on_celling and player.direction.y > 0:
            player.on_celling = False
   

    def run(self):
        #decoration
        self.sky.draw(self.display_surface)
        self.cloud_sprites.draw(self.display_surface,self.world_shift)

        self.bg_palms_sprites.draw(self.display_surface)
        self.bg_palms_sprites.update(self.world_shift)
        
        self.tarrain_sprites.draw(self.display_surface)
        self.tarrain_sprites.update(self.world_shift)

        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        self.crates_sprites.draw(self.display_surface)
        self.crates_sprites.update(self.world_shift)

        
        self.enemies_obstacle_sprites.update(self.world_shift)

        self.enemies_sprites.draw(self.display_surface)
        self.enemies_sprites.update(self.enemies_obstacle_sprites,self.world_shift)

        #player
        self.horixontal_collision()
        self.on_ground_before_verticle_collision = self.player_sprites.sprite.on_floor
        self.vertical_collison()
        self.player_sprites.update()
        self.player_sprites.draw(self.display_surface)
        self.goal_sprite.draw(self.display_surface)
        self.goal_sprite.update(self.world_shift)

        #particle animation
        self.create_landing_particle()
        if self.player_sprites.sprite.jump:
            self.create_jump_particle()

        self.run_particle_animation()
        self.jump_sprtie.draw(self.display_surface)
        self.jump_sprtie.update(self.world_shift)

        #fb palms
        self.fb_palms_sprites.draw(self.display_surface)
        self.fb_palms_sprites.update(self.world_shift)

        self.coins_sprites.draw(self.display_surface)
        self.coins_sprites.update(self.world_shift)
        
        #water
        self.water_sprite.draw(self.display_surface,shift=self.world_shift)

        self.scroll_x()
        # self.camera(self.player_sprites.sprites()[0])
        