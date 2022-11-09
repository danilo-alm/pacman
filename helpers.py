import pygame
import math
from main import SCREEN_WIDTH, SCREEN_HEIGHT, screen
from abc import ABC
from random import choice

class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.init_board()
        self.load_sounds()
        self.init_levels()
        
        self.is_running = True
    
    def check_colision(self):
        if pygame.sprite.spritecollide(pacman_group.sprite, ghosts, False):
            pacman.alive = False
            self.is_running = False
            self.play_sounds('death')
    
    def game_over(self):
        raise NotImplementedError
    
    def event_handler(self, event):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP |  pygame.K_w:
                        pacman.next_direction = 1
                    case pygame.K_RIGHT |  pygame.K_d:
                        pacman.next_direction = 2
                    case pygame.K_DOWN |  pygame.K_s:
                        pacman.next_direction = 3
                    case pygame.K_LEFT |  pygame.K_a:
                        pacman.next_direction = 4
                    
    def init_levels(self):
        # If false, it's chase mode
        self.scatter = None
        self.current_level = 0
        self.num_of_levels = 256
        
        self.time_on_mode_switch = pygame.time.get_ticks()
        self.current_mode_iteration = 0
        
        self.game_mode_intervals = {
            # Time in milliseconds
            1: (7_000, 20_000, 7_000, 20_000, 5_000, 20_000, 5_000),
            2: (7_000, 20_000, 7_000, 20_000, 5_000, 1_020_013, 1),
            3: (7_000, 20_000, 7_000, 20_000, 5_000, 1_020_013, 1),
            4: (7_000, 20_000, 7_000, 20_000, 5_000, 1_020_013, 1),
            5: (5_000, 20_000, 5_000, 20_000, 5_000, 1_020_013, 1)
        }

    def update_game_mode(self):

        if self.scatter is None:
            self.scatter = True
            self.time_on_mode_switch = pygame.time.get_ticks()
            print('scatter')
            return
        
        if self.current_mode_iteration <= 6:
            time_since_mode_switch = pygame.time.get_ticks() - self.time_on_mode_switch
            if time_since_mode_switch > self.game_mode_intervals[self.current_level][self.current_mode_iteration]:
                if self.scatter:
                    self.scatter = False
                    print('chase')
                else:
                    self.scatter = True
                    print('scatter')
                self.time_on_mode_switch = pygame.time.get_ticks()
                self.current_mode_iteration += 1

    def next_level(self):
        self.time_on_level_start = pygame.time.get_ticks()
        self.current_level += 1
        self.current_mode_iteration = 0

    def init_board(self):
        self.rows, self.columns = 31, 28
        
        # width and height of each board tile
        self.pixels = 25 
        self.board = []
        self.board_spaces = self.get_board()
        self.board_positions = self.get_board_positions()
        
        self.pellet_positions = self.filter_positions('pellets')
        self.walls_rects = [pygame.rect.Rect(x, y, 6, 6) for x,y in self.filter_positions('wall')]
        self.power_pellet_positions = self.filter_positions('power_pellets')

    def get_board(self):
        # 0: wall | 1: path | 2: pellets | 3: power pellets | >= 1 are moveable
        return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                [0, 3, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                [0, 3, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 3, 0],
                [0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def get_board_positions(self):
        positions = []
        for y in range(self.rows):
            positions.append(
                # Adding 10, the pixels will be where we want (by trial and error)
                # We're adding 110 to Y not to count the top bar
                [(x * self.pixels + 10, y * self.pixels + 110) for x in range(self.columns)]
            )
        return positions

    def load_images(self):
        for n in range(868):
            filename = 'assets/board_images/tile' + str(n).zfill(3) + '.png'
            image = pygame.image.load(filename).convert()
            self.board.append(pygame.transform.scale(image, (self.pixels, self.pixels)))
        
    def draw_board(self):
        # Column is 4 to account for the top bar
        row, column = 4, 0
        for tile in self.board:
            screen.blit(tile, (self.pixels*column, self.pixels*row))
            column += 1
            if column >= self.columns:
                column = 0
                row += 1  
    
    def filter_positions(self, _filter):
        filtered = []
        filters = {
            'wall': 0,
            'path': 1,
            'pellets': 2,
            'power_pellets': 3
        }
        
        if _filter == 'moveable':
            for y, y_row in enumerate(self.board_spaces):
                for x, item in enumerate(y_row):
                    if self.board_spaces[y][x] >= 1:
                        filtered.append(self.board_positions[y][x])
        else:
            number = filters[_filter]
            for y, y_row in enumerate(self.board_spaces):
                for x, item in enumerate(y_row):
                    if self.board_spaces[y][x] == number:
                        filtered.append(self.board_positions[y][x])
        return filtered
    
    def draw_pellets(self):
        # Normal pellets
        for x,y in self.pellet_positions:
            pygame.draw.rect(screen, 'white', (x, y, 5, 5))
        # Power pellets
        for x,y in self.power_pellet_positions:
            pygame.draw.circle(screen, 'white', (x + 2, y + 2), 7)
    
    def load_sounds(self):
        pygame.mixer.init()
        
        # Munchs
        munch_1 = pygame.mixer.Sound('assets/music/munch_1.wav')
        munch_2 = pygame.mixer.Sound('assets/music/munch_2.wav')
        self.munchs = [munch_1, munch_2]
        self.munch_index = 0
        
        # Siren
        #self.siren_sounds[self.siren_sound_index] = pygame.mixer.Sound('assets/music/siren_1.wav')
        self.siren_sounds = [pygame.mixer.Sound(f'assets/music/siren_{n}.wav') for n in range(1,6)]
        self.siren_sound_index = 0
        self.siren_sounds[self.siren_sound_index].play(loops=-1)
        self.siren_sound_playing = True
        
        # Power pellet
        self.power_pellet_sound = pygame.mixer.Sound('assets/music/power_pellet.wav')
        self.power_pellet_sound_playing = False
        self.time_power_pellet_sound_started = None
        
        # Death
        self.death_1 = pygame.mixer.Sound('assets/music/death_1.wav')
        self.death_2 = pygame.mixer.Sound('assets/music/death_2.wav')
        self.time_death_sound_started = None
    
    def play_death_sound(self):
        if self.time_death_sound_started is None:
            pygame.time.wait(1_000)
            self.time_death_sound_started = pygame.time.get_ticks()
            self.death_1.play()
            
        if pygame.time.get_ticks() - self.time_death_sound_started > 2300:
            self.death_2.play()
            self.time_death_sound_started = None
            pacman.alive = True
    
    def play_sounds(self, sound=None):
        # Update siren sound index
        # TODO
        
        if not pacman.alive:
            if self.siren_sound_playing:
                self.siren_sounds[self.siren_sound_index].stop()
                self.siren_sound_playing = False
        else:
            if not self.siren_sound_playing:
                self.siren_sounds[self.siren_sound_index].play(loops=-1)
                self.siren_sound_playing = True
        
        
        
        if sound:
            match sound:
                case 'munch':
                    self.munchs[self.munch_index].play()
                    if self.munch_index == 0:
                        self.munch_index = 1
                    else:
                        self.munch_index = 0

        if pacman.energized:
            if self.power_pellet_sound_playing:
                # Lower volume of other sounds
                self.munchs[0].set_volume(.35)
                self.munchs[1].set_volume(.35)
                time_since = (pygame.time.get_ticks() - self.time_power_pellet_sound_started) / 1000
                if time_since >= pacman.energized_time:
                    self.power_pellet_sound.stop()
                    self.power_pellet_sound_playing = False
                    pacman.energized = False
                    
                    self.siren_sounds[self.siren_sound_index].play(loops=-1)
                    self.siren_sound_playing = True
                    
                    self.munchs[0].set_volume(1)
                    self.munchs[1].set_volume(1)
            else:
                # Stop siren sound
                self.siren_sounds[self.siren_sound_index].stop()
                self.siren_sound_playing = False
                
                self.power_pellet_sound.play(loops=-1)
                self.time_power_pellet_sound_started = pygame.time.get_ticks()
                self.power_pellet_sound_playing = True
    
    def get_time_since_level_start(self):
        " Return time in miliseconds since level start "
        return pygame.time.get_ticks() - self.time_on_level_start
        
    def update(self):
        self.draw_board()
        self.draw_pellets()

        if self.is_running:
            self.update_game_mode()
            self.check_colision()
        


class Spritesheet(object):
    " https://www.pygame.org/wiki/Spritesheet "
    
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, rectangle, colorkey = None):
        " Loads image from x,y,x+offset,y+offset "
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        " Loads multiple images and returns them as a list"  
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        " Loads a strip of images and returns them as a list "
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


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


def get_linear_distance(a, b):
    # Get linear distance between two points
    return math.hypot(b[0] - a[0], b[1] - a[1])


def rotate(origin, point, angle):
    """ Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians. """
    # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# Load spritesheet element_sheet.png
element_spritesheet = Spritesheet('assets/spritesheets/element_sheet.png')

ghosts = pygame.sprite.Group()
pacman = PacMan()
pacman_group = pygame.sprite.GroupSingle(pacman)
game = Game()

# Creating entities
blinky = Blinky()
pinky = Pinky()
inky = Inky()
clyde = Clyde()

# Start variables
    
game.load_images()
pygame.display.set_caption('Pac-Man')
clock = pygame.time.Clock()

my_ghosts = (blinky, pinky, inky, clyde)
ghosts.add(my_ghosts)
