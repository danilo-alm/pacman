import pygame
from ..entities.blinky import blinky
from ..entities.clyde import clyde
from ..entities.inky import inky
from ..entities.pinky import pinky


ghosts_group = pygame.sprite.Group()
my_ghosts = (blinky, pinky, inky, clyde)
ghosts_group.add(my_ghosts)
