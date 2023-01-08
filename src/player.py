import pygame
from support import import_images_from_folder, wave_value
from settings import player_settings, audio_settings


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.animations = {}
        self.dust_run_particles = []
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = player_settings['animation_speed']
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = player_settings['dust_animation_speed']
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = player_settings['acceleration']
        self.speed = 0
        self.max_speed = player_settings['max_speed']
        self.gravity = player_settings['gravity']
        self.jump_speed = player_settings['jump_speed']
        self.collision_rect = pygame.Rect(self.rect.topleft,
                                          (player_settings['collision_rect_width'],
                                           self.rect.height))

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = player_settings['invincibility_duration']
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('./audio/effects/jump.wav')
        self.jump_sound.set_volume(audio_settings['sfx_volume'] * audio_settings['jump_volume'])
        self.hit_sound = pygame.mixer.Sound('./audio/effects/hit.wav')
        self.hit_sound.set_volume(audio_settings['sfx_volume'])

    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_images_from_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_images_from_folder('./graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.velocity.x += self.acceleration
            self.velocity.x = min(self.velocity.x, self.max_speed)
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.velocity.x -= self.acceleration
            self.velocity.x = max(self.velocity.x, -self.max_speed)
            self.facing_right = False
        else:
            self.velocity = self.velocity * 0.9
            self.direction.x = 0
            self.speed = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(player_settings['damage_penalty'])
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        wave_value()

