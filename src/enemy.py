import pygame
from random import randint
from src.tiles.animated_tile import AnimatedTile
from settings import enemy_settings


class Enemy(AnimatedTile):

    def __init__(self, size, x, y):
        super().__init__(size, x, y, './graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(enemy_settings['speed_min'], enemy_settings['speed_max'])

    def move(self):
        self.rect.x += self.speed

    def orient_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def turn_around(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.orient_image()
