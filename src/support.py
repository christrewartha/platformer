from csv import reader
from settings import tile_size
import pygame
from os import walk
from math import sin


def import_csv_layout(path):

    level_map = []
    with open(path) as raw_map:
        level = reader(raw_map, delimiter=',')
        for row in level:
            level_map.append(list(row))
        return level_map


def import_tiled_image(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for column in range(tile_num_x):
            x = column * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles


def import_images_from_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list


def wave_value():
    value = sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0
