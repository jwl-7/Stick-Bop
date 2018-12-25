import pygame

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700

WHITE  = (253, 250, 243)
BLACK  = ( 45,  43,  46)
BLUE   = (119, 220, 230)

def main():
    pygame.init()
    pygame.mixer.init()

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pygame Test')
    clock = pygame.time.Clock()

    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()