import pygame
from game_data import levels
from support import import_images_from_folder
from decoration import Sky
from easing_functions import QuadEaseInOut


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, path):
        super().__init__()
        self.frames = import_images_from_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):

        self.nodes = None
        self.icon = None

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.moving = False
        self.move_start = pygame.math.Vector2(0, 0)
        self.move_end = pygame.math.Vector2(0, 0)
        self.move_start_time = pygame.time.get_ticks()
        self.move_duration = 750
        self.move_easing = QuadEaseInOut(start=0, end=1, duration=self.move_duration)

        # sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.input_delay_length = 1000

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_start = self.icon.sprite.pos
                self.move_end = self.get_movement_target('next')
                self.move_start_time = pygame.time.get_ticks()
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_start = self.icon.sprite.pos
                self.move_end = self.get_movement_target('previous')
                self.move_start_time = pygame.time.get_ticks()
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_target(self, target):
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return end

    def update_icon_pos(self):
        if self.moving:
            move_time = pygame.time.get_ticks() - self.move_start_time
            if move_time > self.move_duration:
                self.moving = False
                self.icon.sprite.pos = self.move_end
            else:
                easing = self.move_easing.ease(move_time)
                self.icon.sprite.pos = self.move_start + (easing * (self.move_end - self.move_start))

    def input_timer(self):
        if not self.allow_input:
            current_delay = pygame.time.get_ticks() - self.start_time
            if current_delay > self.input_delay_length:
                self.allow_input = True

    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
