import pygame
from settings import tile_size
from src.tiles.terrain_generator import TerrainGenerator
from src.tiles.grass_generator import GrassGenerator
from src.tiles.crate_generator import CrateGenerator
from src.tiles.coin_generator import CoinGenerator
from src.tiles.fg_palm_generator import FGPalmGenerator
from src.tiles.bg_palm_generator import BGPalmGenerator
from src.tiles.enemy_generator import EnemyGenerator
from src.tiles.enemy_constraint_generator import EnemyConstraintGenerator


def create_tile_group(layout, tile_type):
    sprite_group = pygame.sprite.Group()

    generators = {
        'terrain': TerrainGenerator(),
        'grass': GrassGenerator(),
        'crates': CrateGenerator(),
        'coins': CoinGenerator(),
        'fg palms': FGPalmGenerator(),
        'bg palms': BGPalmGenerator(),
        'enemies': EnemyGenerator(),
        'constraints': EnemyConstraintGenerator()
    }

    for row_index, row in enumerate(layout):
        for col_index, val in enumerate(row):
            if val != '-1':
                x = col_index * tile_size
                y = row_index * tile_size

                sprite = generators[tile_type].make_sprite(int(val), x, y)
                sprite_group.add(sprite)

    return sprite_group
