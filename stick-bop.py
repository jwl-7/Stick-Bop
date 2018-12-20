#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stick Bop! is a game made in pygame that was inspired by
the 90s Bop It! toys.
"""

import pygame
import random
from os import path

# asset folder paths
img_dir  = path.join(path.dirname(__file__), 'images')
snd_dir  = path.join(path.dirname(__file__), 'sounds')
font_dir = path.join(path.dirname(__file__), 'fonts')

# game resolution
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700

# game fps
fps = 30

# monokai color palette
white  = (253, 250, 243)
brown  = ( 45,  43,  46)
pink   = (255,  96, 137)
green  = (169, 220, 199)
yellow = (255, 216, 102)
orange = (252, 151, 105)
purple = (171, 157, 244)
blue   = (119, 220, 230)
black  = (  0,   0,   0)

# game constants
score = 0
    
def main():
    pygame.init()
    size   = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    clock  = pygame.time.Clock()
    pygame.display.set_caption('Stick Bop! < TEST >')

    # load assets
    background_image = pygame.image.load(path.join(img_dir, 'stick_pic.png')).convert()
    pygame.mixer.music.load(path.join(snd_dir, 'sword_ahhhh.wav'))
    image2 = pygame.image.load(path.join(img_dir, 'stick_pic_sword.png')).convert()
    game_font = pygame.font.Font(path.join(font_dir, 'OpenSans-Regular.ttf'), 30)

    # display background image
    screen.blit(background_image, [0, 0])

    # loop until user presses close button
    done = False



    # program loop
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # change image when key(left arrow) is pressed -- image stays after keypress
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(0)
                    screen.blit(image2, [0, 0])

            # change image when key(left arrow) is released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    screen.blit(background_image, [0, 0])
             
        # display score to screen into top right corner           
        score_text  = 'Score: ' + str(score)
        score_label = game_font.render(score_text, 1, brown)
        screen.blit(score_label, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - (SCREEN_HEIGHT - 20)))

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    main()