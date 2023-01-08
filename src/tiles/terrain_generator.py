from src.support import import_tiled_image
from src.tiles.static_tile import StaticTile
from src.settings import tile_size


class TerrainGenerator:
    def __init__(self):
        self.terrain_tile_list = import_tiled_image('./graphics/terrain/terrain_tiles.png')

    def make_sprite(self, value, x, y):
        tile_surface = self.terrain_tile_list[value]
        sprite = StaticTile(tile_size, x, y, tile_surface)
        return sprite
