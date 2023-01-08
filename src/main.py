import pygame
import sys
from settings import *
from game import Game

def run_game():
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(clear_colour)
        game.run()

        pygame.display.update()
        clock.tick(tick_rate)


if __name__ == '__main__':
    run_game()

