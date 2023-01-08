from src.tiles.crate import Crate
from src.settings import tile_size


class CrateGenerator:
    def __init__(self):
        pass

    def make_sprite(self, value, x, y):
        sprite = Crate(tile_size, x, y)
        return sprite
