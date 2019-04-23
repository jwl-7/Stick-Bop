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

# for use with PyInstaller
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# asset folder paths
IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')
SND_DIR = os.path.join(os.path.dirname(__file__), 'sounds')
FNT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')

# game constants
SCORE = 0

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

class Assets:
    """Sets up game assets including fonts, images, and sounds.

    Attributes:
        images (dict): Holds all images loaded by the game.
        sounds (dict): Holds all sounds loaded by the game.
        fonts (dict): Holds all fonts loaded by the game.
    """

    images = {}
    sounds = {}
    fonts = {}

    def __init__(self):
        pass

    def load_images(self, directory, colorkey=(0, 0, 0), extensions=('.png', '.jpg', '.bmp')):
        """Loads all images with the specified file extensions.

        Args:
            directory (str): Path to the directory that contains the files.
            colorkey  (tup): Used to set colorkey if no alpha transparency is found in image.
            extensions (tup): The file extensions accepted by the function.

        Returns:
            images (dict): The loaded images.
        """
        images = Assets.images
        for img in os.listdir(directory):
            name, ext = os.path.splitext(img)
            if ext in extensions:
                img = pygame.image.load(os.path.join(directory, img))
                if img.get_alpha():
                    img = img.convert_alpha()
                else:
                    img = img.convert()
                    img.set_colorkey(colorkey)
                images[name] = img
        return images

    def load_sounds(self, directory, extensions=('.ogg', '.mp3', '.wav', '.mdi')):
        """Loads all sounds with the specified file extensions.

        Args:
            directory (str): Path to the directory that contains the files.
            extensions (tup): The file extensions accepted by the function.

        Returns:
            sounds (dict): The loaded images.
        """
        sounds = Assets.sounds
        for snd in os.listdir(directory):
            name, ext = os.path.splitext(snd)
            if ext in extensions:
                sounds[name] = os.path.join(directory, snd)
        return sounds

    def load_fonts(self, directory, extensions=('.ttf')):
        """Loads all fonts with the specified file extension.

        Args:
            directory (str): Path to the directory that contains the files.
            extensions (tup): The file extensions accepted by the function.

        Returns:
            fonts (dict): The loaded fonts.
        """ 
        fonts = Assets.fonts
        for fnt in os.listdir(directory):
            name, ext = os.path.splitext(fnt)
            if ext in extensions:
                fonts[name] = os.path.join(directory, fnt)
        return fonts

    def render_image(self, image, screen_size, screen):
        """Renders an image to the screen at the size of the window.

        Args:
            image (obj): Image that has been loaded by the game.
            screen_size (tup): The width and height of the screen.
            screen (obj): The surface to render the image on.
        Returns:
            image (obj): Image that has been scaled to the screen size.
        """
        if image.get_size() != screen_size:
            image = pygame.transform.smoothscale(image, screen_size, screen)
        return image

    def render_text(self, font, color, text, size, x, y, screen):
        """Draws text in rectangle to surface."""
        text_font = pygame.font.Font(font, size)
        text_surface = text_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        #text = (text_surface, text_rect)
        #return text
        screen.blit(text_surface, text_rect)

    def clear_text(self, font, color, text, size, x, y, screen):
        """Covers text with solid rectangle to surface."""
        text_font = pygame.font.Font(font, size)
        text_surface = text_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        #clear_text = (color, text_rect)
        #return clear_text
        screen.fill(color, text_rect)

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

    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.current = None

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
            #'loss': Loss(),
            #'win': Win(),
            #'drilling': Drilling(),
            #'mining': Mining(),
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

class Loading(State, Assets):
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
        self.load_img = pygame.image.load(os.path.join(IMG_DIR, 'loading.png')).convert()
    
    def load_assets(self):
        """Loads all assets including, fonts, images, and sounds into Assets dictionaries."""
        if self.load == True:
            self.images = self.load_images(IMG_DIR)
            self.sounds = self.load_sounds(SND_DIR)
            self.fonts = self.load_fonts(FNT_DIR)
            self.load = False

    def startup(self):
        pass

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        """Renders loading image and quits state after assets are done loading."""
        self.load_img = self.render_image(self.load_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if time_elapsed >= 200:
            self.load_assets()
        if self.load == False:
            self.done = True

    def draw(self, screen):
        screen.blit(self.load_img, [0, 0])

class Menu(State, Assets):
    """Displays main menu. Allows user to start or quit game.

    Attributes:
        next (str): Specifies the name of the next state.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        self.next = 'start'

    def startup(self):
        self.menu_img = self.images['stick-bop-menu']
        pygame.mixer.music.load(self.sounds['insert-quarter'])
        pygame.mixer.music.play(-1)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True

    def update(self, screen, dt):
        self.menu_img = self.render_image(self.menu_img, self.screen_size, screen)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.menu_img, [0, 0])
        pass

class Start(State, Assets):
    """Displays ready, set, GO! message with sound and starts the game.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        self.next = 'woodchopping'

    def startup(self):
        pygame.mixer.music.stop()
        ready_snd = pygame.mixer.Sound(self.sounds['ready-set-go'])
        ready_snd.play()
        self.start_time = pygame.time.get_ticks()
        self.start_img = self.images['ready']

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.start_img = self.render_image(self.start_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if time_elapsed >= 1000:
            self.start_img = self.images['set']
        if time_elapsed >= 2000:
            self.start_img = self.images['go']
        if time_elapsed >= 3000:
            self.done = True

    def draw(self, screen):
        screen.blit(self.start_img, [0, 0])

class Woodchopping(State, Assets):
    """Woodchopping task.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        #self.next = 'start'

    def startup(self):
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.wood_img = self.images['woodchopping-1']

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if self.right_was_pressed and not self.right_pressed:
                self.wood_img = self.images['woodchopping-1']
                self.right_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if not self.left_pressed:
                self.wood_img = self.images['woodchopping-2']
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                self.right_pressed = False
                self.right_was_pressed = True

    def update(self, screen, dt):
        timer_start = 5
        self.wood_img = self.render_image(self.wood_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        timer_seconds = float(time_elapsed / 1000 % 60)
        timer = round(timer_start - timer_seconds, 1)
        timer_text = 'Timer: ' + str(timer)
        score_text = 'Score: ' + str(self.count)
        self.clear_text(self.fonts['OpenSans-Regular'], WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        self.render_text(self.fonts['OpenSans-Regular'], BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        self.clear_text(self.fonts['OpenSans-Regular'], WHITE, score_text, 40, self.screen_width-150, 0, screen)
        self.render_text(self.fonts['OpenSans-Regular'], BLACK, score_text, 40, self.screen_width-150, 0, screen)

    def draw(self, screen):
        screen.blit(self.wood_img, [0, 0])

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