import sys


import helpers as hp
from game import game
from screen import screen
import pygame
from game import game

sys.path.insert(1, 'groups')
from pacman_group import pacman_group
    
pygame.init()
clock = pygame.time.Clock()
game.load_images()
pygame.display.set_caption('Pac-Man')

# TODO -> 1: Full HD. 2: HD
resolution = 1

# Start level one
hp.game.next_level()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        game.event_handler(event)
    
    # Drawing game board
    game.update()
    
    # Pacman
    hp.pacman_group.draw(screen)
    hp.pacman_group.update()

    # Ghosts
    hp.ghosts.draw(screen)
    hp.ghosts.update()
    
    # Sounds
    game.play_sounds()

    pygame.display.update()
    hp.clock.tick(60)

pygame.quit()
