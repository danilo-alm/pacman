import pygame
import helpers as hp

# TODO:
# IF PACMAN EATS TWO POWER PELLETS SUM THE TIME

# Set window resolution
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 975
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    import pygame
    
    pygame.init()

    # TODO -> 1: Full HD. 2: HD
    resolution = 1

    # Start level one
    hp.game.next_level()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            hp.game.event_handler(event)
        
        # Drawing game board
        hp.game.update()
        
        # Pacman
        hp.pacman_group.draw(screen)
        hp.pacman_group.update()

        # Ghosts
        hp.ghosts.draw(screen)
        hp.ghosts.update()
        
        # Sounds
        hp.game.play_sounds()

        pygame.display.update()
        hp.clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()
