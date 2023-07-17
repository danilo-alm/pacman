from entities.pacman import pacman
from entities.ghost import Ghost
from screen import SCREEN_HEIGHT
from game import game
from screen import SCREEN_WIDTH


class Pinky(Ghost):
    def __init__(self):
        super().__init__()
        self.scatter_target = (150,50)
        self.populate_frames(self.get_sprites(y_position=192))

        self.direction = 2
        self.target_tiles_ahead = 4
        self.pixels_ahead = self.target_tiles_ahead * game.pixels
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.4))
        self.mark_color = 'pink'

    def get_chase_target(self):
        pacman_pos = list(super().get_chase_target())
        # 0 -> Still, 1 -> UP, 2 -> RIGHT, 3 -> DOWN, 4 -> LEFT
        match pacman.current_direction:
            case 1:
                pacman_pos[1] = pacman_pos[1] - self.pixels_ahead
                pacman_pos[0] = pacman_pos[0] - self.pixels_ahead
            case 2:
                pacman_pos[0] = pacman_pos[0] + self.pixels_ahead
            case 3:
                pacman_pos[1] = pacman_pos[1] + self.pixels_ahead
            case 4:
                pacman_pos[0] = pacman_pos[0] -  self.pixels_ahead

        return pacman_pos

    def update(self):
        super().update()
        self.draw_chase_target_mark()


pinky = Pinky()