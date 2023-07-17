import pygame
import sys

sys.path.insert(1, 'entities')
from blinky import blinky
from clyde import clyde
from inky import inky
from pinky import pinky


ghosts_group = pygame.sprite.Group()
my_ghosts = (blinky, pinky, inky, clyde)
ghosts_group.add(my_ghosts)
