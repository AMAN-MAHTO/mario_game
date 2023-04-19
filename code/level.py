import pygame
from settings import *
from support import import_csv_layout,import_cut_graphics,import_graphics
from tiles import Tile,StaticTile,Crate,AnimatedTile,Coin
from enemy import Enemy
from decoration import Sky,Cloud,Water
from player import Player
from particle import ParticleAnimation
from game_data import Level_level,Level_Passed


class Level:
    def __init__(self,current_level,surface,create_overworld,update_coin_count,update_health,what_current_health):
        level_data = Level_level[current_level]
        print(level_data)
        self.current_level = current_level
        self.create_overworld = create_overworld
        self.what_current_health = what_current_health
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

        #player health
        self.update_health = update_health

        #player
        self.player_collided_goal = False
        self.goal_sprite = pygame.sprite.GroupSingle()
        self.player_sprites = pygame.sprite.GroupSingle()
        self.player_layout = import_csv_layout(level_data['player'])
        self.player_setup(self.player_layout)
        
        #score
        self.update_coin_count = update_coin_count
        self.coin_sound = pygame.mixer.Sound("../audio/effects/coin.wav")


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

        #explosion
        self.explosion_sprites = pygame.sprite.Group()


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
                            value = 5
                        else:
                            path = "../graphics/coins/silver"
                            value =1
                        tile_sprite = Coin(TILE_SIZE,x,y,path,value)
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
            offset = player.rect.midbottom - pygame.math.Vector2(12,15)
            self.jump_sprtie.add(ParticleAnimation(offset,'jump'))
        else:
            offset = player.rect.midbottom - pygame.math.Vector2(-12,15)
            self.jump_sprtie.add(ParticleAnimation(offset,'jump'))
    
    def create_landing_particle(self):
        player = self.player_sprites.sprite
        if self.on_ground_before_verticle_collision == False and player.on_floor:
            if player.facing_right:
                offset = player.rect.midbottom - pygame.math.Vector2(15,18)
                self.jump_sprtie.add(ParticleAnimation(offset,'land'))
            else:
                offset = player.rect.midbottom - pygame.math.Vector2(-15,18)
                self.jump_sprtie.add(ParticleAnimation(offset,'land'))
    
    def player_setup(self,layout):
        
        for row_index,row_val in enumerate(layout):
            for col_index,col_value in enumerate(row_val):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col_value != '-1':
                    if col_value == '0':
                        sprite = Player((x,y),self.display_surface,self.update_health)
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
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.tarrain_sprites.sprites() + self.crates_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    player.current_x = player.rect.right
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    player.current_x = player.rect.left

        # if player.on_right and (player.current_x < player.rect.right or player.direction.x <= 0):
        #     player.on_right = False
        # if player.on_left and (player.current_x > player.rect.left or player.direction.x >= 0):
        #     player.on_left = False

    def vertical_collison(self):
        player = self.player_sprites.sprite
        player.apply_gravity()
        
        for sprite in self.tarrain_sprites.sprites() + self.crates_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_celling = True
                if player.direction.y > 0:

                    player.collision_rect.bottom = sprite.rect.top

                    player.on_floor = True
                    player.direction.y = 0

        if player.on_floor and player.direction.y > 1 or player.direction.y < 0:
            player.on_floor = False
        # if player.on_celling and player.direction.y > 0:
        #     player.on_celling = False

    def checking_player_death(self):
        player = self.player_sprites.sprite
        if player.rect.y >= SCREEN_HEIGHT:
            pygame.time.wait(800)
            self.call_overworld()
        

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.call_overworld()
            
    def call_overworld(self):
        self.create_overworld(self.current_level)

    def unlock_level(self):
        self.current_level +=1
        Level_Passed[str(self.current_level)] = True
        self.call_overworld()

    def reached_goal(self):
        player_sprite = self.player_sprites.sprite
        goal_sprtie = self.goal_sprite.sprite
        
        if player_sprite.rect.colliderect(goal_sprtie) and self.player_collided_goal == False:
            pygame.time.wait(1000)
            self.unlock_level()
        self.player_collided_goal = player_sprite.rect.colliderect(goal_sprtie)

    def coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player_sprites.sprite,self.coins_sprites,True)
        if collided_coins:
            for coin in collided_coins:
                self.update_coin_count(coin.value)
                self.coin_sound.play()

    def enimes_collision(self):
        enimes_collided = pygame.sprite.spritecollide(self.player_sprites.sprite,self.enemies_sprites,False)
        
        if enimes_collided:
            for enime in enimes_collided:
                enime_centery = enime.rect.centery
                enime_top = enime.rect.top
                player_bottom = self.player_sprites.sprite.rect.bottom

                if enime_top < player_bottom < enime_centery and self.player_sprites.sprite.direction.y >= 0:
                    self.player_sprites.sprite.direction.y = -15
                    explosion_sprite = ParticleAnimation(enime.rect.center,"explosion")
                    self.explosion_sprites.add(explosion_sprite)
                    enime.kill()
                else:
                    self.player_sprites.sprite.get_damage()
                    self.player_sprites.sprite.direction.y = -8
                    self.player_sprites.sprite.direction.x = enime.direction.x * 8
                    

    def run(self):
        #overworld esc input
        self.input()
        #decoration
        self.sky.draw(self.display_surface)
        self.cloud_sprites.draw(self.display_surface,self.world_shift)

        self.bg_palms_sprites.draw(self.display_surface)
        self.bg_palms_sprites.update(self.world_shift)
        
        self.jump_sprtie.draw(self.display_surface)
        self.jump_sprtie.update(self.world_shift)

        self.tarrain_sprites.draw(self.display_surface)
        self.tarrain_sprites.update(self.world_shift)

        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        self.crates_sprites.draw(self.display_surface)
        self.crates_sprites.update(self.world_shift)

        #enime
        self.enemies_obstacle_sprites.update(self.world_shift)
        self.enemies_sprites.draw(self.display_surface)
        self.enemies_sprites.update(self.enemies_obstacle_sprites,self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)

        #player
        self.horixontal_collision()
        self.on_ground_before_verticle_collision = self.player_sprites.sprite.on_floor
        self.vertical_collison()
        self.player_sprites.update()
        self.player_sprites.draw(self.display_surface)
        self.goal_sprite.draw(self.display_surface)
        self.goal_sprite.update(self.world_shift)
        self.coin_collision()

        #particle animation
        self.create_landing_particle()
        if self.player_sprites.sprite.jump:
            self.create_jump_particle()

        self.run_particle_animation()
        

        #fb palms
        self.fb_palms_sprites.draw(self.display_surface)
        self.fb_palms_sprites.update(self.world_shift)

        self.coins_sprites.draw(self.display_surface)
        self.coins_sprites.update(self.world_shift)
        
        #water
        self.water_sprite.draw(self.display_surface,shift=self.world_shift)

        self.scroll_x()
        self.reached_goal()
        self.checking_player_death()
        self.enimes_collision()
        # self.camera(self.player_sprites.sprites()[0])
        