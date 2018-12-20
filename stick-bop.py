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
IMG_DIR  = path.join(path.dirname(__file__), 'images')
SND_DIR  = path.join(path.dirname(__file__), 'sounds')
FONT_DIR = path.join(path.dirname(__file__), 'fonts')

# game constants
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700
FPS = 30
SCORE = 0

# monokai color palette
WHITE  = (253, 250, 243)
BROWN  = ( 45,  43,  46)
PINK   = (255,  96, 137)
GREEN  = (169, 220, 199)
YELLOW = (255, 216, 102)
ORANGE = (252, 151, 105)
PURPLE = (171, 157, 244)
BLUE   = (119, 220, 230)
BLACK  = (  0,   0,   0)


def game_init():
    pygame.init()
    pygame.mixer.init()

def game_menu():
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    menu_snd = pygame.mixer.music.load(path.join(SND_DIR, 'piano-lofi-rain.ogg'))
    pygame.mixer.music.play(-1)

    menu_img = pygame.image.load(path.join(IMG_DIR, 'game-menu.png')).convert()
    menu_img = pygame.transform.scale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)

    screen.blit(menu_img, [0, 0])
    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            pygame.display.update()

    print('GAME READY TO START')

def draw_text(surface, text, size, x, y):
    game_font = pygame.font.Font(path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
    text_surface = game_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    game_init()

    # setup game window
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Stick Bop!')

    # load assets
    image1 = pygame.image.load(path.join(IMG_DIR, 'stick-pic.png')).convert()
    image2 = pygame.image.load(path.join(IMG_DIR, 'stick-pic-sword.png')).convert()

    # MAIN GAME LOOP
    #----------------------------------------------------------------

    # loop until user presses close button
    running = True
    menu_display = True

    # program loop
    while running:
        if menu_display:
            game_menu()
            pygame.mixer.music.stop()

            ready_snd = pygame.mixer.Sound(path.join(SND_DIR, 'ready-set-go.ogg'))
            ready_snd.play()

            screen.fill(WHITE)
            draw_text(screen, 'READY', 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            pygame.display.update()
            pygame.time.wait(1000)

            screen.fill(WHITE)
            draw_text(screen, 'SET', 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            pygame.display.update()
            pygame.time.wait(1000)

            screen.fill(WHITE)
            draw_text(screen, 'GO!', 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            pygame.display.update()
            pygame.time.wait(1000)

            menu_display = False

        clock.tick(FPS)
        screen.blit(image1, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # change image when key(left arrow) is pressed -- image stays after keypress
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sword_snd = pygame.mixer.Sound(path.join(SND_DIR, 'sword_ahhhh.wav'))
                    sword_snd.play()
                    screen.blit(image2, [0, 0])

            # change image when key(left arrow) is released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    screen.blit(image1, [0, 0])
             
        # display score to screen into top right corner           
        score_text = 'Score: ' + str(SCORE)
        draw_text(screen, score_text, 40, SCREEN_WIDTH - (SCREEN_WIDTH / 6), 0)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()