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
import os

from data import tools

# for use with PyInstaller
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# asset folder paths
IMG_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'images')
SND_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
FNT_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'fonts')

# monokai color palette
WHITE = (253, 250, 243)
BLACK = (45, 43, 46)
RED = (255, 96, 137)
GREEN = (169, 220, 199)
BLUE = (119, 220, 230)
YELLOW = (255, 216, 102)
ORANGE = (252, 151, 105)
PURPLE = (171, 157, 244)

settings = {
    'screen_size': (900, 700),
    'screen_width': 900,
    'screen_height': 700,
    'screen_max_width': 1920,
    'screen_max_height': 1080,
    'fps': 60,
    'title': 'Stick Bop!'  
}

class State(object):
    """Parent class for various game states.

    Attributes:
        done (bool): State completion status.
        quit (bool): State exit status.
        next (none): Holds the value of the next state.
        current (none): Holds the value of the current state.
    """
    score = 0
    count = 0
    task_list = ['drilling', 'mining', 'woodchopping']

    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.current = None

    def track_check(self, score):
        music_track = 'neon-runner'
        if score == 25:
            music_track = 'neon-runner-x125'
        elif score == 50:
            music_track = 'neon-runner-x150'
        elif score == 75:
            music_track = 'neon-runner-x175'
        elif score == 100:
            self.next = 'win'
            self.done = True
        return music_track

    def music_check(self, score, track):
        new_music_scores = [0, 25, 50, 75]
        if score in new_music_scores:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(-1)

    def count_check(self, count, timer):
        if count >= 5 and timer > 0:
            State.score += 1
            task_done_snd = pygame.mixer.Sound(tools.sounds['task-done'])
            pygame.mixer.Channel(0).play(task_done_snd)
            self.done = True
            print('task_complete')
        elif timer <= 0:
            self.next = 'loss'
            self.done = True

    def timer_check(self, score):
        if score >= 0:
            timer_start = 5
        elif score >= 25:
            timer_start = 4.5
        elif score >= 50:
            timer_start = 4
        elif score >= 75:
            timer_start = 3.5
        return timer_start


class StateController:
    """Controls and sets up the game settings, game states, and main game loop.
    
    Args:
        **settings (dict): Game display settings.

    Attributes:
        done (bool): State completion status.
        display_info (obj): Provides information about the default display mode.
        screen_max_width (int): Maximum screen width allowed based on display_info.
        screen_max_height (int): Maximum screen height allowed based on display_height.
        screen (obj): Initializes display surface.
        caption (obj): Sets the window title.
        clock (obj): Initializes clock object to help track time.
        states (dict): The various game states.
    """

    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.display_info = pygame.display.Info()
        self.screen_max_width = self.display_info.current_w
        self.screen_max_height = self.display_info.current_h
        self.screen = pygame.display.set_mode(self.screen_size)
        self.caption = pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.states = {
            'loading': Loading(),
            'menu': Menu(),
            'start': Start(),
            'loss': Loss(),
            'win': Win(),
            'drilling': Drilling(),
            'mining': Mining(),
            'woodchopping': Woodchopping()
        }
    
    def setup_states(self, start_state):
        """Sets the initial state."""
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def flip_state(self):
        """Flips to the next state."""
        self.state.done = False
        current = self.state_name
        self.state_name = self.state.next
        self.state = self.states[self.state_name]
        self.state.startup()
        self.state.current = current

    def update(self, dt):
        """Checks for state flip and updates current state.

        Args:
            dt (int): Milliseconds since last frame.
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def event_loop(self):
        """Events are passed for handling the current state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    def game_loop(self):
        """This is the main game loop."""
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()

class Loading(State):
    """Displays loading image. Loads all assets including fonts, images, and sounds.

    Attributes:
        next (str): Specifies the name of the next state.
        load (bool): Determines whether or not the assets should be loaded.
        start_time (int): Start timer used for delaying asset loading.
        load_img (obj): Loading image that displays while the assets load.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        self.next = 'menu'
        self.load = True
        self.start_time = pygame.time.get_ticks()
        files_path = [os.path.abspath(x) for x in os.listdir()]
        print(os.path.join(IMG_DIR, 'loading.png'))
        self.load_img = pygame.image.load(os.path.join(IMG_DIR, 'loading.png')).convert()
    
    def load_assets(self):
        """Loads all assets including, fonts, images, and sounds into Assets dictionaries."""
        if self.load == True:
            tools.images = tools.load_images(IMG_DIR)
            tools.sounds = tools.load_sounds(SND_DIR)
            tools.fonts = tools.load_fonts(FNT_DIR)
            self.load = False

    def startup(self):
        pass

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        """Renders loading image and quits state after assets are done loading."""
        self.load_img = tools.render_image(self.load_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if time_elapsed >= 200:
            self.load_assets()
        if self.load == False:
            self.done = True

    def draw(self, screen):
        screen.blit(self.load_img, [0, 0])

class Menu(State):
    """Displays main menu. Allows user to start or quit game.

    Attributes:
        next (str): Specifies the name of the next state.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        self.next = 'start'

    def startup(self):
        self.menu_img = tools.images['stick-bop-menu']
        pygame.mixer.music.load(tools.sounds['insert-quarter'])
        pygame.mixer.music.play(-1)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True

    def update(self, screen, dt):
        self.menu_img = tools.render_image(self.menu_img, self.screen_size, screen)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.menu_img, [0, 0])
        pass

class Start(State):
    """Displays ready, set, GO! message with sound and starts the game.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        pygame.mixer.music.stop()
        ready_snd = pygame.mixer.Sound(tools.sounds['ready-set-go'])
        ready_snd.play()
        self.start_time = pygame.time.get_ticks()
        self.start_img = tools.images['ready']

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.start_img = tools.render_image(self.start_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if time_elapsed >= 1000:
            self.start_img = tools.images['set']
        if time_elapsed >= 2000:
            self.start_img = tools.images['go']
        if time_elapsed >= 3000:
            self.done = True

    def draw(self, screen):
        screen.blit(self.start_img, [0, 0])

class Woodchopping(State):
    """Woodchopping task.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        print(self.next)
        self.count = 0
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.wood_img = tools.images['woodchopping-1']
        game_snd = self.track_check(self.score)
        self.music_check(self.score, tools.sounds[game_snd])

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if self.right_was_pressed and not self.right_pressed:
                self.wood_img = tools.images['woodchopping-1']
                self.right_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if not self.left_pressed:
                self.wood_img = tools.images['woodchopping-2']
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                self.right_pressed = False
                self.right_was_pressed = True

    def update(self, screen, dt):
        self.wood_img = tools.render_image(self.wood_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(self.timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(self.score)
        tools.clear_text(tools.fonts['OpenSans-Regular'], WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], WHITE, score_text, 40, self.screen_width-150, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, score_text, 40, self.screen_width-150, 0, screen)
        tools.draw_progress_bar(self.screen_width-100, self.screen_height/4, self.count*20, screen)
        self.count_check(self.count, timer)

    def draw(self, screen):
        screen.blit(self.wood_img, [0, 0])

class Drilling(State):
    """Drilling task.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        print(self.next)
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.drill_img = tools.images['drilling-1']
        game_snd = self.track_check(self.score)
        self.music_check(self.score, tools.sounds[game_snd])

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drill_img = tools.images['drilling-2']
            self.count += 1
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.drill_img = tools.images['drilling-1']

    def update(self, screen, dt):
        self.drill_img = tools.render_image(self.drill_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(self.timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(self.score)
        tools.clear_text(tools.fonts['OpenSans-Regular'], WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], WHITE, score_text, 40, self.screen_width-150, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, score_text, 40, self.screen_width-150, 0, screen)
        tools.draw_progress_bar(self.screen_width-100, self.screen_height/4, self.count*20, screen)
        self.count_check(self.count, timer)

    def draw(self, screen):
        screen.blit(self.drill_img, [0, 0])

class Mining(State):
    """Mining task.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        print(self.next)
        self.count = 0
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.mine_img = tools.images['mining-1']
        game_snd = self.track_check(self.score)
        self.music_check(self.score, tools.sounds[game_snd])

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if self.right_was_pressed and not self.right_pressed:
                self.mine_img = tools.images['mining-1']
                self.right_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if not self.left_pressed:
                self.mine_img = tools.images['mining-2']
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                self.right_pressed = False
                self.right_was_pressed = True

    def update(self, screen, dt):
        self.mine_img = tools.render_image(self.mine_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(self.timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(self.score)
        tools.clear_text(tools.fonts['OpenSans-Regular'], WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], WHITE, score_text, 40, self.screen_width-150, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, score_text, 40, self.screen_width-150, 0, screen)
        tools.draw_progress_bar(self.screen_width-100, self.screen_height/4, self.count*20, screen)
        self.count_check(self.count, timer)

    def draw(self, screen):
        screen.blit(self.mine_img, [0, 0])

class Loss(State):
    """Loss state.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        self.next = 'menu'

    def startup(self):
        self.loss_img = tools.images['game-over']
        pygame.mixer.music.stop()
        pygame.mixer.music.load(tools.sounds['piano-lofi-rain'])
        pygame.mixer.music.play(-1)
        self.score_text = 'Final Score: ' + str(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True

    def update(self, screen, dt):
        self.loss_img = tools.render_image(self.loss_img, self.screen_size, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], BLACK, self.score_text, 100, self.screen_width/2, self.screen_height/2.5, screen)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.loss_img, [0, 0])

class Win(State):
    """Win state.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        self.next = 'menu'

    def startup(self):
        self.win_img = tools.images['winner']
        pygame.mixer.music.stop()
        pygame.mixer.music.load(tools.sounds['future-grid'])
        pygame.mixer.music.play(-1)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True

    def update(self, screen, dt):
        self.win_img = tools.render_image(self.win_img, self.screen_size, screen)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.win_img, [0, 0])

def main():
    """Initialize pygame and run game."""
    pygame.init()
    game = StateController(**settings)
    game.setup_states('loading')
    game.game_loop()
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()