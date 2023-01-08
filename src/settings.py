vertical_tile_number = 11
tile_size = 64

screen_height = vertical_tile_number * tile_size
screen_width = 1200

clear_colour = 'grey'
tick_rate = 60

player_settings = {
    'animation_speed': 0.15,
    'dust_animation_speed': 0.15,
    'acceleration': 0.5,
    'max_speed': 5,
    'gravity': 0.8,
    'jump_speed': -16,
    'collision_rect_width': 50,
    'invincibility_duration': 500,
    'damage_penalty': -10
}

enemy_settings = {
    'speed_max': 5,
    'speed_min': 3
}

audio_settings = {
    'sfx_volume': 0.25,
    'music_volume': 0.25,
    'jump_volume': 0.5
}

decoration_settings = {
    'water_height': 25,
    'water_tile_width': 192
}
