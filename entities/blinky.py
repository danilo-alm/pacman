from entities.ghost import Ghost
from screen import SCREEN_HEIGHT
from screen import SCREEN_WIDTH


class Blinky(Ghost):
    def __init__(self):
        super().__init__()
        self.scatter_target = (650,50)
        self.populate_frames(self.get_sprites(y_position=144))
        self.out_of_house = True

        self.direction = 4
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.4))
        self.mark_color = 'red'

    def update(self):
        super().update()
        self.draw_chase_target_mark()


blinky = Blinky()
