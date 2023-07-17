import pygame
import sys

sys.path.insert(1, 'entities')
from pacman import pacman


pacman_group = pygame.sprite.GroupSingle(pacman)