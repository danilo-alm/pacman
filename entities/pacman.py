import pygame

from spritesheet import element_spritesheet
from game import game
from ghost_group import my_ghosts

from screen import SCREEN_HEIGHT
from screen import SCREEN_WIDTH


class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.load_frames()

        # Power pellet
        self.energized = False
        self.energized_time = 10
        self.alive = True

        self.playing_death_anitation = False

        # 0 -> Still, 1 -> UP, 2 -> RIGHT, 3 -> DOWN, 4 -> LEFT
        self.current_direction = 0
        self.next_direction = 0

        # The direction pacman is facing. Will be important for ghost's targets
        self.facing = 0

        # Pixels per frame
        self.speed = 3

        self.image = self.frames_right[3]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * .575))

    def play_death_animation(self):
        if not self.playing_death_anitation:
            self.playing_death_anitation = True
            self.frame_index = 0
        self.frame_index += .08

        if self.frame_index >= 10.9:
            self.playing_death_anitation = False
            return

        self.image = self.death_frames[int(self.frame_index)]

    def load_frames(self):
        # Loading sprite sheets
        coordinates = ((240,72,38,46), (288,72,44,46), (338,72,46,46))
        self.frames_right = [
            pygame.transform.scale(i, (39,39)) for i in element_spritesheet.images_at(coordinates)
        ]

        # Adding a duplicate frame to make animation easier
        # `frames_right` -> Pacman is facing right...
        self.frames_right.append(self.frames_right[1])
        self.frames_up = [pygame.transform.rotate(frame, 90) for frame in self.frames_right]
        self.frames_left = [pygame.transform.rotate(frame, 180) for frame in self.frames_right]
        self.frames_down = [pygame.transform.rotate(frame, 270) for frame in self.frames_right]
        self.frame_index = 0

        coordinates = ((98,172,20,14), (122,172,20,14), (146,172,20,14), (170,172,20,14),
                       (194,172,24,14), (218,172,20,16), (244,172,20,18), (270,172,20,16),
                       (296,172,20,16), (322,172,20,16), (338,172,20,18))
        self.death_frames = [
            pygame.transform.scale(i, (30,30)) for i in element_spritesheet.images_at(coordinates)
        ]

    def is_direction_valid(self, direction):
        x, y = self.rect.x, self.rect.y

        # How many tiles ahead we'll check for colision
        tiles_ahead = 6

        # 0 -> Still, 1 -> UP, 2 -> RIGHT, 3 -> DOWN, 4 -> LEFT
        match direction:
            case 1: y -= tiles_ahead
            case 2: x += tiles_ahead
            case 3: y += tiles_ahead
            case 4: x -= tiles_ahead

        pacman_future_rect = pygame.rect.Rect(x, y, self.rect.width, self.rect.height)
        for rect in game.walls_rects:
            if rect.colliderect(pacman_future_rect):
                return False
        return True

    def update_current_diretion(self):
        if self.current_direction != 0:
            pacman.facing = self.current_direction

        if self.next_direction != 0:
            if self.is_direction_valid(self.next_direction):
                self.current_direction = self.next_direction

        if not self.is_direction_valid(self.current_direction):
            self.current_direction = 0

    def movement(self):
        match self.current_direction:
            case 1: self.rect.y -= self.speed
            case 2: self.rect.x += self.speed
            case 3: self.rect.y += self.speed
            case 4: self.rect.x -= self.speed

    def animation_state(self):
        self.frame_index += .25

        if self.current_direction == 0:
            self.image = self.frames_right[2]
            return

        if self.frame_index >= 4:
            self.frame_index = 0

        match self.current_direction:
            case 1: self.image = self.frames_up[int(self.frame_index)]
            case 2: self.image = self.frames_right[int(self.frame_index)]
            case 3: self.image = self.frames_down[int(self.frame_index)]
            case 4: self.image = self.frames_left[int(self.frame_index)]

    def eat_pellet(self):
        for index, pellet in enumerate(game.pellet_positions):
            if self.rect.collidepoint(pellet):
                game.pellet_positions.pop(index)
                game.play_sounds('munch')

        for index, power_pellet in enumerate(game.power_pellet_positions):
            if self.rect.collidepoint(power_pellet):
                game.power_pellet_positions.pop(index)
                self.energized = True

                for ghost in my_ghosts: ghost.turn_around()

    def update(self):
        if self.alive:
            self.update_current_diretion()
            self.movement()
            self.eat_pellet()
            self.animation_state()
        else:
            self.play_death_animation()
            game.play_death_sound()


pacman = PacMan()