from entities.pacman import pacman
from entities.ghost import Ghost
from helpers import get_linear_distance
from screen import SCREEN_HEIGHT
from game import game
from screen import SCREEN_WIDTH


class Clyde(Ghost):
    def __init__(self):
        super().__init__()
        self.scatter_target = (15, SCREEN_HEIGHT - 100)
        self.populate_frames(self.get_sprites(y_position=216))

        self.maximum_distance = game.pixels * 8
        self.direction = 4
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.4))
        self.mark_color = 'orange'

    def get_chase_target(self):
        try:
            if get_linear_distance(pacman.rect.center, self.rect.center) < self.maximum_distance:
                return pacman.rect.center
            else:
                return self.scatter_target
        except AttributeError:
            return 5,5

    def update(self):
        super().update()
        self.draw_chase_target_mark()


clyde = Clyde()