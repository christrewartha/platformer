from src.tiles.palm import Palm
from src.settings import tile_size


class FGPalmGenerator:
    def __init__(self):
        pass

    def make_sprite(self, value, x, y):
        sprite = None
        if value == 2:
            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_small', 38)
        if value == 1:
            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_large', 64)
        return sprite
