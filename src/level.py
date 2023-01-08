import pygame
from support import import_csv_layout
from settings import tile_size, screen_height, screen_width, decoration_settings
from src.tiles.static_tile import StaticTile
from tile_support import create_tile_group
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):

        self.current_level = current_level
        level_data = levels[current_level]
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld
        self.has_content = level_data['has_content']
        self.display_surface = surface

        if not self.has_content:
            level_content = level_data['content']

            self.font = pygame.font.Font(None, 40)
            self.text_surf = self.font.render(level_content, True, 'White')
            self.text_rect = self.text_surf.get_rect(center=(screen_width / 2, screen_height / 2))

        else:
            self.world_shift = 0

            # audio
            self.coin_sound = pygame.mixer.Sound('./audio/effects/coin.wav')
            self.stomp_sound = pygame.mixer.Sound('./audio/effects/stomp.wav')

            self.level_objects = {
                'constraints': None,
                'bg palms': None,
                'terrain': None,
                'crates': None,
                'coins': None,
                'grass': None,
                'player': None,
                'fg palms': None,
                'enemies': None
            }

            self.level_width = 0
            for object_type in list(self.level_objects.keys()):
                csv_layout = import_csv_layout(level_data[object_type])
                if object_type == 'player':
                    self.player_setup(csv_layout, change_health)
                else:
                    self.level_width = len(csv_layout[0]) * tile_size
                    self.level_objects[object_type] = create_tile_group(csv_layout, object_type)

            # decoration
            self.sky = Sky(8)
            self.water = Water(screen_height - decoration_settings['water_height'], self.level_width)
            self.clouds = Clouds(400, self.level_width, 20)

            # user interface
            self.change_coins = change_coins

    def player_setup(self, layout, change_health):
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.explosion_sprites = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('./graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_constraint_check(self):
        for enemy in self.level_objects['enemies'].sprites():
            if pygame.sprite.spritecollide(enemy, self.level_objects['constraints'], False):
                enemy.turn_around()

    def run(self):
        # run the entire game / level
        self.input()

        if not self.has_content:
            self.display_surface.blit(self.text_surf, self.text_rect)
        else:
            self.player_update_logic()
            self.enemy_constraint_check()

            # decoration
            self.sky.draw(self.display_surface)
            self.clouds.draw(self.display_surface, self.world_shift)

            for object_type in list(self.level_objects.keys()):
                if object_type == 'player':
                    self.dust_sprite.draw(self.display_surface)
                    self.player.draw(self.display_surface)
                    self.goal.draw(self.display_surface)
                elif object_type == 'constraints':
                    self.level_objects[object_type].update(self.world_shift)
                elif object_type == 'enemies':
                    self.level_objects[object_type].update(self.world_shift)
                    self.level_objects[object_type].draw(self.display_surface)
                    self.explosion_sprites.update(self.world_shift)
                    self.explosion_sprites.draw(self.display_surface)
                else:
                    self.level_objects[object_type].update(self.world_shift)
                    self.level_objects[object_type].draw(self.display_surface)

            # water
            self.water.draw(self.display_surface, self.world_shift)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        collideable_sprites = self.level_objects['terrain'].sprites() + \
                              self.level_objects['crates'].sprites() + \
                              self.level_objects['fg palms'].sprites()

        for sprite in collideable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.velocity.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                elif player.velocity.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collideable_sprites = self.level_objects['terrain'].sprites() + \
                              self.level_objects['crates'].sprites() + \
                              self.level_objects['fg palms'].sprites()

        for sprite in collideable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.level_objects['coins'], True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.level_objects['enemies'], False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def player_update_logic(self):
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.scroll_x()
        self.goal.update(self.world_shift)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()
        # dust particles
        self.dust_sprite.update(self.world_shift)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
