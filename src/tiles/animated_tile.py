from src.tiles.tile import Tile
from random import randint
from src.support import import_images_from_folder


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)

        self.frames = import_images_from_folder(path)
        self.frame_index = randint(0, len(self.frames) - 1)
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, shift_x):
        super().update(shift_x)
        self.animate()

