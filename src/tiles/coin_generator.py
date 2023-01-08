from src.tiles.coin import Coin
from src.settings import tile_size


class CoinGenerator:
    def __init__(self):
        pass

    def make_sprite(self, value, x, y):
        sprite = None
        if value == 0:
            sprite = Coin(tile_size, x, y, './graphics/coins/gold', 5)
        if value == 1:
            sprite = Coin(tile_size, x, y, './graphics/coins/silver', 1)
        return sprite
