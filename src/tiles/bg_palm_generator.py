from src.tiles.palm import Palm
from src.settings import tile_size


class BGPalmGenerator:
    def __init__(self):
        pass

    def make_sprite(self, value, x, y):
        sprite = Palm(tile_size, x, y, './graphics/terrain/palm_bg', 64)
        return sprite
