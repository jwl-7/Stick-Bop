#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Authors: Jonathan Lusk and Brandon Hough

"""
Stick Bop! is a game made in pygame that was inspired by the 90s Bop It! toy.
"""

import pygame
import random
import sys
from os import path

# for use with PyInstaller
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# asset folder paths
IMG_DIR  = path.join(path.dirname(__file__), 'images')
SND_DIR  = path.join(path.dirname(__file__), 'sounds')
FONT_DIR = path.join(path.dirname(__file__), 'fonts')

# game constants
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700
SCREEN_MAX_WIDTH  = 1920
SCREEN_MAX_HEIGHT = 1080
FPS   = 60
SCORE =  0

# monokai color palette
WHITE  = (253, 250, 243)
BLACK  = ( 45,  43,  46)
RED    = (255,  96, 137)
GREEN  = (169, 220, 199)
BLUE   = (119, 220, 230)
YELLOW = (255, 216, 102)
ORANGE = (252, 151, 105)
PURPLE = (171, 157, 244)

def game_init():
    """Initialize Pygame and mixer module."""

    global SCREEN_MAX_WIDTH
    global SCREEN_MAX_HEIGHT

    pygame.init()
    pygame.mixer.init()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    display_info = pygame.display.Info()
    SCREEN_MAX_WIDTH = display_info.current_w
    SCREEN_MAX_HEIGHT = display_info.current_h
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Stick Bop!')

def draw_text(surface, color, text, size, x, y):
    """Draw text in rectangle to surface."""

    game_font = pygame.font.Font(path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
    text_surface = game_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def clear_text(surface, color, text, size, x, y):
    """Cover text with solid rectangle to surface."""

    game_font = pygame.font.Font(path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
    text_surface = game_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.fill(color, text_rect)

def draw_progress_bar(surface, x, y, progress):
    """Draw a colored progress bar with outline to surface."""

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
    """Display start menu."""

    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    menu_snd = pygame.mixer.music.load(path.join(SND_DIR, 'insert-quarter.ogg'))
    pygame.mixer.music.play(-1)

    menu_img = pygame.image.load(path.join(IMG_DIR, 'stick-bop-menu.png')).convert()
    menu_img = pygame.transform.smoothscale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)

    screen.blit(menu_img, [0, 0])
    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
            if SCREEN_WIDTH <= SCREEN_MAX_WIDTH and SCREEN_WIDTH <= SCREEN_MAX_HEIGHT:
                SCREEN_WIDTH += 100
                SCREEN_HEIGHT += 100
                size = SCREEN_WIDTH, SCREEN_HEIGHT
                screen = pygame.display.set_mode(size)
                menu_img = pygame.image.load(path.join(IMG_DIR, 'stick-bop-menu.png')).convert()
                menu_img = pygame.transform.smoothscale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(menu_img, [0, 0])
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            if SCREEN_WIDTH >= 500 and SCREEN_HEIGHT >= 300: 
                SCREEN_WIDTH -= 100
                SCREEN_HEIGHT -= 100
                size = SCREEN_WIDTH, SCREEN_HEIGHT
                screen = pygame.display.set_mode(size)
                menu_img = pygame.image.load(path.join(IMG_DIR, 'stick-bop-menu.png')).convert()
                menu_img = pygame.transform.smoothscale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(menu_img, [0, 0])
        else:
            pygame.display.update()

def game_ready():
    """Display ready, set, GO! message with sound."""

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()

    pygame.mixer.music.stop()
    ready_snd = pygame.mixer.Sound(path.join(SND_DIR, 'ready-set-go.ogg'))
    ready_snd.play()

    ready_img = pygame.image.load(path.join(IMG_DIR, 'ready.png')).convert()
    ready_img = pygame.transform.smoothscale(ready_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(ready_img, [0, 0])
    pygame.display.update()
    pygame.time.wait(1000)

    set_img = pygame.image.load(path.join(IMG_DIR, 'set.png')).convert()
    set_img = pygame.transform.smoothscale(set_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(set_img, [0, 0])
    pygame.display.update()
    pygame.time.wait(1000)

    go_img = pygame.image.load(path.join(IMG_DIR, 'go.png')).convert()
    go_img = pygame.transform.smoothscale(go_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(go_img, [0, 0])
    pygame.display.update()
    pygame.time.wait(1000)

def task_drilling():
    """Start and display drilling work task."""

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    drilling1_img = pygame.image.load(path.join(IMG_DIR, 'drilling-1.png')).convert()
    drilling1_img = pygame.transform.smoothscale(drilling1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(drilling1_img, [0, 0])

    global SCORE
    count = 0
    start_time = pygame.time.get_ticks()

    if SCORE >= 75:
        timer_start = 3.5
    elif SCORE >= 50:
        timer_start = 4
    elif SCORE >= 25:
        timer_start = 4.5
    elif SCORE >= 0:
        timer_start = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                drilling2_img = pygame.image.load(path.join(IMG_DIR, 'drilling-2.png')).convert()
                drilling2_img = pygame.transform.smoothscale(drilling2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(drilling2_img, [0, 0])
                count += 1
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                drilling1_img = pygame.image.load(path.join(IMG_DIR, 'drilling-1.png')).convert()
                drilling1_img = pygame.transform.smoothscale(drilling1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(drilling1_img, [0, 0])

        time_elapsed = pygame.time.get_ticks() - start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(SCORE)

        clear_text(screen, WHITE, timer_text, 40, SCREEN_WIDTH / 2, 0)
        clear_text(screen, WHITE, score_text, 40, SCREEN_WIDTH - 150, 0)
        draw_text(screen, BLACK, timer_text, 40, SCREEN_WIDTH / 2, 0)
        draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - 150, 0)
        draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

        if count >= 5 and timer > 0:
            SCORE += 1
            return True
        elif timer <= 0:
            return False

        pygame.display.update()
        
def task_mining():
    """Start and display mining work task."""

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    mining1_img = pygame.image.load(path.join(IMG_DIR, 'mining-1.png')).convert()
    mining1_img = pygame.transform.smoothscale(mining1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(mining1_img, [0, 0])

    global SCORE
    count = 0
    start_time = pygame.time.get_ticks()

    if SCORE >= 75:
        timer_start = 3.5
    elif SCORE >= 50:
        timer_start = 4
    elif SCORE >= 25:
        timer_start = 4.5
    elif SCORE >= 0:
        timer_start = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                mining2_img = pygame.image.load(path.join(IMG_DIR, 'mining-2.png')).convert()
                mining2_img = pygame.transform.smoothscale(mining2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(mining2_img, [0, 0])
                count += 1
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                mining1_img = pygame.image.load(path.join(IMG_DIR, 'mining-1.png')).convert()
                mining1_img = pygame.transform.smoothscale(mining1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(mining1_img, [0, 0])

        time_elapsed = pygame.time.get_ticks() - start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(SCORE)

        clear_text(screen, WHITE, timer_text, 40, SCREEN_WIDTH / 2, 0)
        clear_text(screen, WHITE, score_text, 40, SCREEN_WIDTH - 150, 0)
        draw_text(screen, BLACK, timer_text, 40, SCREEN_WIDTH / 2, 0)
        draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - 150, 0)
        draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

        if count >= 5 and timer > 0:
            SCORE += 1
            return True
        elif timer <= 0:
            return False

        pygame.display.update()

def task_woodchopping():
    """Start and display woodchopping work task."""

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    woodchopping1_img = pygame.image.load(path.join(IMG_DIR, 'woodchopping-1.png')).convert()
    woodchopping1_img = pygame.transform.smoothscale(woodchopping1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(woodchopping1_img, [0, 0])

    global SCORE
    count = 0
    start_time = pygame.time.get_ticks()

    if SCORE >= 75:
        timer_start = 3.5
    elif SCORE >= 50:
        timer_start = 4
    elif SCORE >= 25:
        timer_start = 4.5
    elif SCORE >= 0:
        timer_start = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                woodchopping2_img = pygame.image.load(path.join(IMG_DIR, 'woodchopping-2.png')).convert()
                woodchopping2_img = pygame.transform.smoothscale(woodchopping2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(woodchopping2_img, [0, 0])
                count += 1
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                woodchopping1_img = pygame.image.load(path.join(IMG_DIR, 'woodchopping-1.png')).convert()
                woodchopping1_img = pygame.transform.smoothscale(woodchopping1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(woodchopping1_img, [0, 0])

        time_elapsed = pygame.time.get_ticks() - start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(SCORE)

        clear_text(screen, WHITE, timer_text, 40, SCREEN_WIDTH / 2, 0)
        clear_text(screen, WHITE, score_text, 40, SCREEN_WIDTH - 150, 0)
        draw_text(screen, BLACK, timer_text, 40, SCREEN_WIDTH / 2, 0)
        draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - 150, 0)
        draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

        if count >= 5 and timer > 0:
            SCORE += 1
            return True
        elif timer <= 0:
            return False

        pygame.display.update()

def game_end():
    """Display game over message and final score."""

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()

    menu_snd = pygame.mixer.music.load(path.join(SND_DIR, 'piano-lofi-rain.ogg'))
    pygame.mixer.music.play(-1)

    gameover_img = pygame.image.load(path.join(IMG_DIR, 'game-over.png')).convert()
    gameover_img = pygame.transform.smoothscale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(gameover_img, [0, 0])

    score_text = 'Final Score: ' + str(SCORE)
    draw_text(screen, BLACK, score_text, 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_RETURN:
                main()
        else:
            pygame.display.update()

def game_win():
    """Display winner image and message."""

    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()

    menu_snd = pygame.mixer.music.load(path.join(SND_DIR, 'future-grid.ogg'))
    pygame.mixer.music.play(-1)

    gameover_img = pygame.image.load(path.join(IMG_DIR, 'winner.png')).convert()
    gameover_img = pygame.transform.smoothscale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(gameover_img, [0, 0])

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_RETURN:
                main()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            pygame.display.update()

def main():
    """Initialize game and run main game loop."""

    game_init()
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    global SCORE
    task_list = ['drilling', 'mining', 'woodchopping']

    running = True
    menu_display = True
    task_completed = True

    SCORE = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if menu_display:
            game_menu()
            game_ready()
            menu_display = False
            game_snd = pygame.mixer.music.load(path.join(SND_DIR, 'neon-runner.ogg'))
            pygame.mixer.music.play(-1)
        elif task_completed:
            if SCORE > 0:
                task_done_snd = pygame.mixer.Sound(path.join(SND_DIR, 'task-done.ogg'))
                pygame.mixer.Channel(0).play(task_done_snd)

            task = random.choice(task_list)

            if task == 'drilling':
                task_completed = task_drilling()
            elif task == 'mining':
                task_completed = task_mining()
            elif task == 'woodchopping':
                task_completed = task_woodchopping()
        elif not task_completed:
            game_end()

        if SCORE == 25:
            game_snd_x25 = pygame.mixer.music.load(path.join(SND_DIR, 'neon-runner-x125.ogg'))
            pygame.mixer.music.play(-1)
        elif SCORE == 50:
            game_snd_x50 = pygame.mixer.music.load(path.join(SND_DIR, 'neon-runner-x150.ogg'))
            pygame.mixer.music.play(-1)
        elif SCORE == 75:
            game_snd_x75 = pygame.mixer.music.load(path.join(SND_DIR, 'neon-runner-x175.ogg'))
            pygame.mixer.music.play(-1)
        elif SCORE == 100:
            game_win()
                
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()