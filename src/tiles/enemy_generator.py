from src.enemy import Enemy
from src.settings import tile_size


class EnemyGenerator:
    def __init__(self):
        pass
    
    def make_sprite(self, value, x, y):
        sprite = Enemy(tile_size, x, y)
        return sprite
