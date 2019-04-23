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

class State(object):
    """Parent class for various game states.

    Attributes:
        done (bool): State completion status.
        quit (bool): State exit status.
        next (none): Holds the value of the next state.
        current (none): Holds the value of the current state.
    """

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
            #'start': Start(),
            #'loss': Loss(),
            #'win': Win(),
            #'drilling': Drilling(),
            #'mining': Mining(),
            #'woodchopping': Woodchopping()
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
        """Displays loading image."""
        screen.blit(self.load_img, [0, 0])

class Menu(State, Assets):
    """Displays main menu. Allows user to start or quit game.

    Attributes:
        next (str): Specifies the name of the next state.
    """

    def __init__(self):
        State.__init__(self)
        self.__dict__.update(settings)
        #self.next = 'start'

    def startup(self):
        self.menu_img = self.images['stick-bop-menu']

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.menu_img = self.render_image(self.menu_img, self.screen_size, screen)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.menu_img, [0, 0])
        pass

def main():
    """Initialize pygame and run game."""
    pygame.init()
    game = StateController(**settings)
    game.setup_states('loading')
    game.game_loop()
    pygame.quit()
    sys.exit()

#----------------------------------------------------------------------------------------
#
# EVERYTHING BELOW WILL BE REFACTORED ~~~~
#
#----------------------------------------------------------------------------------------

class ZZZ:
    """This class deals with every part of the game."""

    def game_init(self):
        """Initialize Pygame and mixer module."""

        global SCREEN_MAX_WIDTH
        global SCREEN_MAX_HEIGHT
        global SCREEN_SIZE

        pygame.init()
        pygame.mixer.init()
        display_info = pygame.display.Info()
        SCREEN_MAX_WIDTH = display_info.current_w
        SCREEN_MAX_HEIGHT = display_info.current_h
        pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Stick Bop!')

    def load_images(self, path_dir):
        """Load the images and return them in a dictionary."""

        global IMG_DICT
        global SCREEN_WIDTH
        global SCREEN_HEIGHT

        screen = pygame.display.get_surface()
        
        for filename in os.listdir(path_dir):
            if filename.endswith('.png'):
                path = os.path.join(path_dir, filename)
                key = filename[:-4]
                IMG_DICT[key] = pygame.image.load(path).convert()
                #IMG_DICT[key] = pygame.transform.smoothscale(IMG_DICT[key], (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
        #return IMG_DICT

    def draw_text(self, surface, color, text, size, x, y):
        """Draw text in rectangle to surface."""

        game_font = pygame.font.Font(os.path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
        text_surface = game_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def clear_text(self, surface, color, text, size, x, y):
        """Cover text with solid rectangle to surface."""

        game_font = pygame.font.Font(os.path.join(FONT_DIR, 'OpenSans-Regular.ttf'), size)
        text_surface = game_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.fill(color, text_rect)

    def draw_progress_bar(self, surface, x, y, progress):
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

    def game_menu(self):
        """Display start menu."""

        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        global SCREEN_SIZE

        screen = pygame.display.get_surface()
        menu_snd = pygame.mixer.music.load(os.path.join(SND_DIR, 'insert-quarter.ogg'))
        pygame.mixer.music.play(-1)

        menu_img = pygame.image.load(os.path.join(IMG_DIR, 'stick-bop-menu.png')).convert()
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
                    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT
                    screen = pygame.display.set_mode(SCREEN_SIZE)
                    menu_img = pygame.image.load(os.path.join(IMG_DIR, 'stick-bop-menu.png')).convert()
                    menu_img = pygame.transform.smoothscale(menu_img, (SCREEN_SIZE), screen)
                    screen.blit(menu_img, [0, 0])
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                if SCREEN_WIDTH >= 500 and SCREEN_HEIGHT >= 300: 
                    SCREEN_WIDTH -= 100
                    SCREEN_HEIGHT -= 100
                    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT
                    screen = pygame.display.set_mode(SCREEN_SIZE)
                    menu_img = pygame.image.load(os.path.join(IMG_DIR, 'stick-bop-menu.png')).convert()
                    menu_img = pygame.transform.smoothscale(menu_img, (SCREEN_SIZE), screen)
                    screen.blit(menu_img, [0, 0])
            else:
                pygame.display.update()

    def game_ready(self):
        """Display ready, set, GO! message with sound."""

        global SCREEN_SIZE

        screen = pygame.display.get_surface()

        pygame.mixer.music.stop()
        ready_snd = pygame.mixer.Sound(os.path.join(SND_DIR, 'ready-set-go.ogg'))
        ready_snd.play()

        ready_img = pygame.image.load(os.path.join(IMG_DIR, 'ready.png')).convert()
        ready_img = pygame.transform.smoothscale(ready_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
        screen.blit(ready_img, [0, 0])
        pygame.display.update()
        pygame.time.wait(1000)

        set_img = pygame.image.load(os.path.join(IMG_DIR, 'set.png')).convert()
        set_img = pygame.transform.smoothscale(set_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
        screen.blit(set_img, [0, 0])
        pygame.display.update()
        pygame.time.wait(1000)

        go_img = pygame.image.load(os.path.join(IMG_DIR, 'go.png')).convert()
        go_img = pygame.transform.smoothscale(go_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
        screen.blit(go_img, [0, 0])
        pygame.display.update()
        pygame.time.wait(1000)

    def task_drilling(self):
        """Start and display drilling work task."""

        global SCREEN_SIZE

        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        drilling1_img = pygame.image.load(os.path.join(IMG_DIR, 'drilling-1.png')).convert()
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
                    drilling2_img = pygame.image.load(os.path.join(IMG_DIR, 'drilling-2.png')).convert()
                    drilling2_img = pygame.transform.smoothscale(drilling2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(drilling2_img, [0, 0])
                    count += 1
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    drilling1_img = pygame.image.load(os.path.join(IMG_DIR, 'drilling-1.png')).convert()
                    drilling1_img = pygame.transform.smoothscale(drilling1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(drilling1_img, [0, 0])

            time_elapsed = pygame.time.get_ticks() - start_time
            timer_seconds = float(time_elapsed / 1000 % 60)
            timer = round(timer_start - timer_seconds, 1)
            timer_text = 'Timer: ' + str(timer)
            score_text = 'Score: ' + str(SCORE)

            self.clear_text(screen, WHITE, timer_text, 40, SCREEN_WIDTH / 2, 0)
            self.clear_text(screen, WHITE, score_text, 40, SCREEN_WIDTH - 150, 0)
            self.draw_text(screen, BLACK, timer_text, 40, SCREEN_WIDTH / 2, 0)
            self.draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - 150, 0)
            self.draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

            if count >= 5 and timer > 0:
                SCORE += 1
                return True
            elif timer <= 0:
                return False

            pygame.display.update()
            
    def task_mining(self):
        """Start and display mining work task."""

        global SCREEN_SIZE

        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        mining1_img = pygame.image.load(os.path.join(IMG_DIR, 'mining-1.png')).convert()
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
                    mining2_img = pygame.image.load(os.path.join(IMG_DIR, 'mining-2.png')).convert()
                    mining2_img = pygame.transform.smoothscale(mining2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(mining2_img, [0, 0])
                    count += 1
                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    mining1_img = pygame.image.load(os.path.join(IMG_DIR, 'mining-1.png')).convert()
                    mining1_img = pygame.transform.smoothscale(mining1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(mining1_img, [0, 0])

            time_elapsed = pygame.time.get_ticks() - start_time
            timer_seconds = float(time_elapsed / 1000 % 60)
            timer = round(timer_start - timer_seconds, 1)
            timer_text = 'Timer: ' + str(timer)
            score_text = 'Score: ' + str(SCORE)

            self.clear_text(screen, WHITE, timer_text, 40, SCREEN_WIDTH / 2, 0)
            self.clear_text(screen, WHITE, score_text, 40, SCREEN_WIDTH - 150, 0)
            self.draw_text(screen, BLACK, timer_text, 40, SCREEN_WIDTH / 2, 0)
            self.draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - 150, 0)
            self.draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

            if count >= 5 and timer > 0:
                SCORE += 1
                return True
            elif timer <= 0:
                return False

            pygame.display.update()

    def task_woodchopping(self):
        """Start and display woodchopping work task."""

        global SCREEN_SIZE

        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        woodchopping1_img = pygame.image.load(os.path.join(IMG_DIR, 'woodchopping-1.png')).convert()
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
                    woodchopping2_img = pygame.image.load(os.path.join(IMG_DIR, 'woodchopping-2.png')).convert()
                    woodchopping2_img = pygame.transform.smoothscale(woodchopping2_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(woodchopping2_img, [0, 0])
                    count += 1
                elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                    woodchopping1_img = pygame.image.load(os.path.join(IMG_DIR, 'woodchopping-1.png')).convert()
                    woodchopping1_img = pygame.transform.smoothscale(woodchopping1_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
                    screen.blit(woodchopping1_img, [0, 0])

            time_elapsed = pygame.time.get_ticks() - start_time
            timer_seconds = float(time_elapsed / 1000 % 60)
            timer = round(timer_start - timer_seconds, 1)
            timer_text = 'Timer: ' + str(timer)
            score_text = 'Score: ' + str(SCORE)

            self.clear_text(screen, WHITE, timer_text, 40, SCREEN_WIDTH / 2, 0)
            self.clear_text(screen, WHITE, score_text, 40, SCREEN_WIDTH - 150, 0)
            self.draw_text(screen, BLACK, timer_text, 40, SCREEN_WIDTH / 2, 0)
            self.draw_text(screen, BLACK, score_text, 40, SCREEN_WIDTH - 150, 0)
            self.draw_progress_bar(screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT / 4, count * 20)

            if count >= 5 and timer > 0:
                SCORE += 1
                return True
            elif timer <= 0:
                return False

            pygame.display.update()

    def game_end(self):
        """Display game over message and final score."""

        global SCREEN_SIZE

        screen = pygame.display.get_surface()

        menu_snd = pygame.mixer.music.load(os.path.join(SND_DIR, 'piano-lofi-rain.ogg'))
        pygame.mixer.music.play(-1)

        gameover_img = pygame.image.load(os.path.join(IMG_DIR, 'game-over.png')).convert()
        gameover_img = pygame.transform.smoothscale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
        screen.blit(gameover_img, [0, 0])

        score_text = 'Final Score: ' + str(SCORE)
        self.draw_text(screen, BLACK, score_text, 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5)

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

    def game_win(self):
        """Display winner image and message."""

        global SCREEN_SIZE
        
        screen = pygame.display.get_surface()

        menu_snd = pygame.mixer.music.load(os.path.join(SND_DIR, 'future-grid.ogg'))
        pygame.mixer.music.play(-1)

        gameover_img = pygame.image.load(os.path.join(IMG_DIR, 'winner.png')).convert()
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
    
    def loop(self, screen):
        """Main game loop."""

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
                self.game_menu()
                self.game_ready()
                menu_display = False
                game_snd = pygame.mixer.music.load(os.path.join(SND_DIR, 'neon-runner.ogg'))
                pygame.mixer.music.play(-1)
            elif task_completed:
                if SCORE > 0:
                    task_done_snd = pygame.mixer.Sound(os.path.join(SND_DIR, 'task-done.ogg'))
                    pygame.mixer.Channel(0).play(task_done_snd)

                task = random.choice(task_list)

                if task == 'drilling':
                    task_completed = self.task_drilling()
                elif task == 'mining':
                    task_completed = self.task_mining()
                elif task == 'woodchopping':
                    task_completed = self.task_woodchopping()
            elif not task_completed:
                self.game_end()

            if SCORE == 25:
                game_snd_x25 = pygame.mixer.music.load(os.path.join(SND_DIR, 'neon-runner-x125.ogg'))
                pygame.mixer.music.play(-1)
            elif SCORE == 50:
                game_snd_x50 = pygame.mixer.music.load(os.path.join(SND_DIR, 'neon-runner-x150.ogg'))
                pygame.mixer.music.play(-1)
            elif SCORE == 75:
                game_snd_x75 = pygame.mixer.music.load(os.path.join(SND_DIR, 'neon-runner-x175.ogg'))
                pygame.mixer.music.play(-1)
            elif SCORE == 100:
                self.game_win()
                    
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
        quit()

if __name__ == '__main__':
    main()