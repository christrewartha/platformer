import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.original_x = x
        self.original_y = y
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift_x):
        self.rect.x += shift_x
