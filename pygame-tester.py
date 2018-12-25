import pygame

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700

WHITE  = (253, 250, 243)
BLACK  = ( 45,  43,  46)
BLUE   = (119, 220, 230)

def main():
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    pygame.init()
    pygame.mixer.init()

    # get user's screen resolution
    display_info_object = pygame.display.Info()
    display_max_width = display_info_object.current_w
    display_max_height = display_info_object.current_h

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                if SCREEN_WIDTH <= display_max_width and SCREEN_WIDTH <= display_max_height:
                    SCREEN_WIDTH += 100
                    SCREEN_HEIGHT += 100
                    size = SCREEN_WIDTH, SCREEN_HEIGHT
                    screen = pygame.display.set_mode(size)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                if SCREEN_WIDTH >= 700 and SCREEN_HEIGHT >= 500: 
                    SCREEN_WIDTH -= 100
                    SCREEN_HEIGHT -= 100
                    size = SCREEN_WIDTH, SCREEN_HEIGHT
                    screen = pygame.display.set_mode(size)
                
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()