"""
STICK BOP! --- IN DEVELOPMENT
"""

import pygame
import random

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700

# monokai color palette
white  = (253, 250, 243)
brown  = ( 45,  43,  46)
pink   = (255,  96, 137)
green  = (169, 220, 199)
yellow = (255, 216, 102)
orange = (252, 151, 105)
purple = (171, 157, 244)
blue   = (119, 220, 230)

score = 0

def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Stick Bop! Test~~")

    # loop until user presses close button
    done = False

    # manage how fast screen updates
    clock = pygame.time.Clock()

    # program loop
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        screen.fill(white)
        clock.tick(60)

        is_purple = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_purple = not is_purple

        if is_purple:
            color = purple
        else: 
            color = blue

        pygame.draw.rect(screen, color, pygame.Rect(200, 200, 200, 200))

        # update screen
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()