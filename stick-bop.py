#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stick Bop! is a game made in pygame that was inspired by the 90s Bop It! toy.
"""

import pygame
import random
import sys
from os import path

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# asset folder paths
IMG_DIR  = path.join(path.dirname(__file__), 'images')
SND_DIR  = path.join(path.dirname(__file__), 'sounds')
FONT_DIR = path.join(path.dirname(__file__), 'fonts')

# game constants
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700
FPS   = 30
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
    pygame.init()
    pygame.mixer.init()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
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
        if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
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
    """Start and display jackhammer work task."""
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    jackhammer1_img = pygame.image.load(path.join(IMG_DIR, 'jackhammer-1.png')).convert()
    jackhammer1_img = pygame.transform.scale(jackhammer1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(jackhammer1_img, [0, 0])

    global SCORE
    count = 0
    timer_start = 5
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jackhammer2_img = pygame.image.load(path.join(IMG_DIR, 'jackhammer-2.png')).convert()
                jackhammer2_img = pygame.transform.scale(jackhammer2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(jackhammer2_img, [0, 0])
                count += 1
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                jackhammer1_img = pygame.image.load(path.join(IMG_DIR, 'jackhammer-1.png')).convert()
                jackhammer1_img = pygame.transform.scale(jackhammer1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(jackhammer1_img, [0, 0])

        time_elapsed = pygame.time.get_ticks() - start_time
        timer_seconds = int(time_elapsed / 1000 % 60)
        timer = timer_start - timer_seconds
        timer_text = 'TIMER: ' + str(timer)
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

def task_axe():
    """Start and display axe work task."""
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    axe1_img = pygame.image.load(path.join(IMG_DIR, 'axe-1.png')).convert()
    axe1_img = pygame.transform.scale(axe1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(axe1_img, [0, 0])

    global SCORE
    count = 0
    timer_start = 5
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                axe2_img = pygame.image.load(path.join(IMG_DIR, 'axe-2.png')).convert()
                axe2_img = pygame.transform.scale(axe2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                screen.blit(axe2_img, [0, 0])
                count += 1
                
        time_elapsed = pygame.time.get_ticks() - start_time
        timer_seconds = int(time_elapsed / 1000 % 60)
        timer = timer_start - timer_seconds
        timer_text = 'TIMER: ' + str(timer)
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
    gameover_img = pygame.transform.scale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(gameover_img, [0, 0])

    score_text = 'Final Score: ' + str(SCORE)
    draw_text(screen, BLACK, score_text, 70, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)
    draw_text(screen, BLACK, 'Press [ESC] to QUIT', 40, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)

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
        else:
            pygame.display.update()

def game_win():
    """Display winner image and message."""
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.get_surface()

    menu_snd = pygame.mixer.music.load(path.join(SND_DIR, 'strum-strums.ogg'))
    pygame.mixer.music.play(-1)

    gameover_img = pygame.image.load(path.join(IMG_DIR, 'winner.png')).convert()
    gameover_img = pygame.transform.scale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    screen.blit(gameover_img, [0, 0])

    draw_text(screen, BLACK, 'Press [ESC] to QUIT', 40, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)
    draw_text(screen, BLACK, 'Press [T] to Try Again!', 40, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 1.5)+50)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            pygame.display.update()

def main():
    """Initialize game and run main game loop."""
    game_init()
    clock = pygame.time.Clock()

    task_list = ['jackhammer', 'axe']

    running = True
    menu_display = True
    task_completed = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if menu_display:
            game_menu()
            game_ready()
            menu_display = False
        elif not menu_display:
            task = random.choice(task_list)

            if task == 'jackhammer':
                task_completed = task_jackhammer()
            elif task == 'axe':
                task_completed = task_axe()

        if task_completed:
            jackhammer_display = True
        elif not task_completed:
            game_end()

        if SCORE >= 10:
            game_win()
                
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()