import pygame
from screen import screen
from entities.pacman import pacman
from groups.ghosts import ghosts_group
from groups.pacman import pacman_group


class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.init_board()
        self.load_sounds()
        self.init_levels()

        self.is_running = True

    def check_colision(self):
        if pygame.sprite.spritecollide(pacman_group.sprite, ghosts_group, False):
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


game = Game()