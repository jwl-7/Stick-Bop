#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stick Bop! is a game made in pygame that was inspired by the 90s Bop It! toy.
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

def draw_text(surface, color, text, size, x, y):
    game_font = pygame.font.Font(path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
    text_surface = game_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def clear_text(surface, color, text, size, x, y):
    game_font = pygame.font.Font(path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
    text_surface = game_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.fill(color, text_rect)

def draw_progress_bar(surface, x, y, progress):
    BAR_LENGTH = 40
    BAR_HEIGHT = 400

    progress = max(progress, 0)
    fill = (progress / 100) * BAR_HEIGHT
    fill_rect = pygame.Rect(x, y, BAR_LENGTH, fill)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    pygame.draw.rect(surface, GREEN, outline_rect)
    pygame.draw.rect(surface, WHITE, fill_rect)
    pygame.draw.rect(surface, BLACK, outline_rect, 4)

def game_menu():
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
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
        elif event.type == pygame.QUIT:
            pygame.quit()
        else:
            pygame.display.update()

def game_ready():
    pygame.mixer.music.stop()

    ready_snd = pygame.mixer.Sound(path.join(SND_DIR, 'ready-set-go.ogg'))
    ready_snd.play()

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()

    ready_img = pygame.image.load(path.join(IMG_DIR, 'ready.png')).convert()
    ready_img = pygame.transform.scale(ready_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(ready_img, [0, 0])
    pygame.display.update()
    pygame.time.wait(1000)

    set_img = pygame.image.load(path.join(IMG_DIR, 'set.png')).convert()
    set_img = pygame.transform.scale(set_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(set_img, [0, 0])
    pygame.display.update()
    pygame.time.wait(1000)

    go_img = pygame.image.load(path.join(IMG_DIR, 'go.png')).convert()
    go_img = pygame.transform.scale(go_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(go_img, [0, 0])
    pygame.display.update()
    pygame.time.wait(1000)

def task_jackhammer():
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    jackhammer1_img = pygame.image.load(path.join(IMG_DIR, 'jackhammer-1.png')).convert()
    jackhammer1_img = pygame.transform.scale(jackhammer1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(jackhammer1_img, [0, 0])

    count = 0
    count_down = 5
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jackhammer2_img = pygame.image.load(path.join(IMG_DIR, 'jackhammer-2.png')).convert()
                    jackhammer2_img = pygame.transform.scale(jackhammer2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(jackhammer2_img, [0, 0])
                    count += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    jackhammer1_img = pygame.image.load(path.join(IMG_DIR, 'jackhammer-1.png')).convert()
                    jackhammer1_img = pygame.transform.scale(jackhammer1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(jackhammer1_img, [0, 0])

        time_since = pygame.time.get_ticks() - start_time
        millis = int(time_since)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        count_down_timer = count_down - seconds
        count_msg = 'TIMER: ' + str(count_down_timer)

        clear_text(screen, WHITE, count_msg, 40, SCREEN_WIDTH / 2, 0)
        draw_text(screen, BLACK, count_msg, 40, SCREEN_WIDTH / 2, 0)
        draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

        if count >= 5 and count_down_timer > 0:
            screen.fill(WHITE)
            draw_text(screen, BLUE, 'YOU WIN!', 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            break
        elif count_down_timer <= 0:
            screen.fill(BLUE)
            draw_text(screen, WHITE, 'GAME OVER!', 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
            break
        
        pygame.display.update()

def main():
    game_init()

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Stick Bop!')

    running = True
    menu_display = True
    scene_jackhammer = False

    while running:
        if menu_display:
            game_menu()
            #game_ready()
            menu_display = False
            scene_jackhammer = True

        if scene_jackhammer:
            task_jackhammer()
            scene_jackhammer = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        score_text = 'Score: ' + str(SCORE)
        draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - (SCREEN_WIDTH / 6), 0)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()