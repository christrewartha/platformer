from src.support import import_tiled_image
from src.tiles.static_tile import StaticTile
from src.settings import tile_size


class GrassGenerator:
    def __init__(self):
        self.grass_tile_list = import_tiled_image('./graphics/decoration/grass/grass.png')

    def make_sprite(self, value, x, y):
        tile_surface = self.grass_tile_list[value]
        sprite = StaticTile(tile_size, x, y, tile_surface)

        return sprite
