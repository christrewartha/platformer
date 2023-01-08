from src.tiles.tile import Tile
from src.settings import tile_size


class EnemyConstraintGenerator:
    def __init__(self):
        pass

    def make_sprite(self, value, x, y):
        sprite = Tile(tile_size, x, y)
        return sprite
