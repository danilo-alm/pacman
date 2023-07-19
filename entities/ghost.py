from helpers import element_spritesheet, game, get_linear_distance, pacman
from screen import screen
import pygame
from abc import ABC
from random import choice

from screen import SCREEN_HEIGHT, SCREEN_WIDTH

class Ghost(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        # x,y positions the ghost will target in scatter mode and chase mode
        self.scatter_target = (None, None)
        self.chase_target = self.get_chase_target()
        self.current_target = (None, None)
        self.frightened = False
        self.spawn = True
        self.eaten = False
        self.house = pygame.rect.Rect(SCREEN_WIDTH / 2.55, SCREEN_HEIGHT/2.3, 150, 80)

        self.frame_index = 0
        self.frames_frightened = self.get_sprites(
            from_nth_image=8, to_nth_image=11, y_position=96
        )

        # 0 -> Still, 1 -> UP, 2 -> RIGHT, 3 -> DOWN, 4 -> LEFT
        self.direction = 0
        self.speed = 3

        # Used only displaying the target on game
        self.mark_color = 'green'

    def turn_around(self):
        # Sometimes, the ghosts will turn 180 degrees. Let's make a function for that
        match self.direction:
            case 1: self.direction = 3
            case 2: self.direction = 4
            case 3: self.direction = 1
            case 4: self.direction = 2
        pacman.has_eaten_pellet += 1

    def populate_frames(self, sprites):
        self.frames_right = sprites[:2]
        self.frames_down = sprites[2:4]
        self.frames_left = sprites[4:6]
        self.frames_up = sprites[6:8]
        self.image = self.frames_left[self.frame_index]

    def get_sprites(self, from_nth_image=0, to_nth_image=None, y_position=0):
        if to_nth_image is None:
            to_nth_image = from_nth_image + 8

        image_coordinates = [(i * 24, y_position, 22, 22) for i in range(from_nth_image, to_nth_image)]
        sprites = element_spritesheet.images_at(image_coordinates)
        return [pygame.transform.scale(i, (pacman.rect.width, pacman.rect.height)) for i in sprites]

    def get_chase_target(self):
        return pacman.rect.center

    def draw_chase_target_mark(self):
        # Draw ghosts current target on screen
        pygame.draw.rect(screen, self.mark_color, (*self.current_target, 10, 10))

    def update_target(self):
        if pacman.energized:
            self.frightened = True
        else:
            self.frightened = False

        if game.scatter:
            self.current_target = self.scatter_target
        else:
            self.current_target = self.get_chase_target()
        # match game.game_mode:
        #     case 'scatter':
        #         self.current_target = self.scatter_target
        #     case 'chase':
        #         self.current_target = self.get_chase_target()

    def animate(self):

        self.frame_index += .25
        if self.frame_index >= 2:
            self.frame_index = 0

        if self.frightened:
            self.image = self.frames_frightened[int(self.frame_index)]
            return

        # 0 -> Still, 1 -> UP, 2 -> RIGHT, 3 -> DOWN, 4 -> LEFT
        match self.direction:
            case 1:
                self.image = self.frames_up[int(self.frame_index)]
            case 2:
                self.image = self.frames_right[int(self.frame_index)]
            case 3:
                self.image = self.frames_down[int(self.frame_index)]
            case 4:
                self.image = self.frames_left[int(self.frame_index)]

    def movement(self):

        # Without increasing the dimensions a little bit, our collision
        # detection won't work :(
        increase = 3

        # Current position
        x, y = self.rect.x, self.rect.y

        # 1 -> UP, 2 -> RIGHT, 3 -> DOWN, 4 -> LEFT
        # Element 0 is UP, 1 is RIGHT, and so on...
        current_direction = self.direction
        directions = [True for i in range(4)]
        best_route = None

        for index, item in enumerate(directions):
            new_y = None
            new_x = None
            match index:
                case 0:
                    # If we're not going DOWN, check for UP
                    if self.direction == 3:
                        directions[index] = False
                        continue
                    new_y = y - self.speed
                case 1:
                    # If we're not going LEFT, check for RIGHT
                    if self.direction == 4:
                        directions[index] = False
                        continue
                    new_x = x + self.speed
                case 2:
                    # If we're not going UP, check for DOWN
                    if self.direction == 1:
                        directions[index] = False
                        continue
                    new_y = y + self.speed
                case other:
                    # If we're not going RIGHT, check for LEFT
                    if self.direction == 2:
                        directions[index] = False
                        continue
                    new_x = x - self.speed

            ghost_future_rect = None
            if index % 2:
                ghost_future_rect = pygame.rect.Rect(new_x, y, self.rect.width+increase , self.rect.height+increase)
            else:
                ghost_future_rect = pygame.rect.Rect(x, new_y, self.rect.width+increase , self.rect.height+increase)

            for rect in game.walls_rects:
                if rect.colliderect(ghost_future_rect):
                    directions[index] = False
                    break
            if directions[index]:
                dist = get_linear_distance(ghost_future_rect.center, self.current_target)
                if best_route is None or dist < best_route[1]:
                    best_route = [index + 1, dist]

        if self.frightened:
            # TODO: GET THEM TO TURN AROUND ONCE ENTERING MODE

            # Get random direction
            options = [1,2,3,4]
            for index, boolean in enumerate(directions):
                if boolean is False:
                    options.remove(index + 1)
            best_route[0] = choice(options)

        match best_route[0]:
            case 1:
                self.rect.y -= self.speed
            case 2:
                self.rect.x += self.speed
            case 3:
                self.rect.y += self.speed
            case 4:
                self.rect.x -= self.speed

        self.direction = best_route[0]

    def update(self):
        if game.is_running:
            self.update_target()
            self.movement()
            self.animate()
            if pacman.has_eaten_pellet > 0:
                self.turn_around()