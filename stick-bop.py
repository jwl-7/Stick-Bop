"""
STICK BOP! --- IN DEVELOPMENT
"""

import pygame
import random
import sys

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

background_image_filename = 'background_picture.png'

score = 0

def main():
    pygame.init()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Stick Bop! Test~~")

    #drawing background
    background = pygame.image.load(background_image_filename).convert()
    screen.blit(background, (0,0))

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

        is_purple = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_purple = not is_purple

        if is_purple:
            color = purple
        else: 
            color = blue

        # update full-screen
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()