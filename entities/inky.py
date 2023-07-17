from blinky import blinky
from pinky import Pinky
from helpers import get_linear_distance
from screen import SCREEN_HEIGHT
from helpers import rotate
import math

from screen import SCREEN_WIDTH


class Inky(Pinky):
    def __init__(self):
        super().__init__()
        self.scatter_target = (SCREEN_WIDTH- 20, SCREEN_HEIGHT - 20)
        self.populate_frames(self.get_sprites(from_nth_image=8, y_position=192))

        self.direction = 2
        self.target_tiles_ahead = 2
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.4))
        self.mark_color = 'cyan'

    def get_chase_target(self):
        two_tiles_ahead = super().get_chase_target()
        blinky_pos = list(blinky.rect.center)
        tile_to_blinky = get_linear_distance(two_tiles_ahead, blinky_pos)

        return rotate(blinky_pos, two_tiles_ahead, math.pi)

    def update(self):
        super().update()
        self.draw_chase_target_mark()


inky = Inky()