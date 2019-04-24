import pygame
import random
import os
from . import state_machine
from . import tools

class Loading(state_machine.State):
    """Displays loading image. Loads all assets including fonts, images, and sounds.

    Attributes:
        next (str): Specifies the name of the next state.
        load (bool): Determines whether or not the assets should be loaded.
        start_time (int): Start timer used for delaying asset loading.
        load_img (obj): Loading image that displays while the assets load.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)
        self.next = 'menu'
        self.load = True
        self.start_time = pygame.time.get_ticks()
        self.load_img = pygame.image.load(os.path.join(tools.IMG_DIR, 'loading.png')).convert()
    
    def load_assets(self):
        """Loads all assets including, fonts, images, and sounds into Assets dictionaries."""
        if self.load == True:
            tools.images = tools.load_images(tools.IMG_DIR)
            tools.sounds = tools.load_sounds(tools.SND_DIR)
            tools.fonts = tools.load_fonts(tools.FNT_DIR)
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

class Menu(state_machine.State):
    """Displays main menu. Allows user to start or quit game.

    Attributes:
        next (str): Specifies the name of the next state.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)
        self.next = 'start'

    def startup(self):
        self.menu_img = tools.images['stick-bop-menu']
        tools.play_music(tools.sounds['insert-quarter'])

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

class Start(state_machine.State):
    """Displays ready, set, GO! message with sound and starts the game.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        pygame.mixer.music.stop()
        tools.play_sound(tools.sounds['ready-set-go'])
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

class Woodchopping(state_machine.State):
    """Woodchopping task.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        self.count = 0
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.wood_img = tools.images['woodchopping-1']
        self.score_check(self.score)

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
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, score_text, 40, self.screen_width-150, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, score_text, 40, self.screen_width-150, 0, screen)
        tools.draw_progress_bar(self.screen_width-100, self.screen_height/4, self.count*20, screen)
        self.count_check(self.count, timer)

    def draw(self, screen):
        screen.blit(self.wood_img, [0, 0])

class Drilling(state_machine.State):
    """Drilling task.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.drill_img = tools.images['drilling-1']
        self.score_check(self.score)

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
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, score_text, 40, self.screen_width-150, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, score_text, 40, self.screen_width-150, 0, screen)
        tools.draw_progress_bar(self.screen_width-100, self.screen_height/4, self.count*20, screen)
        self.count_check(self.count, timer)

    def draw(self, screen):
        screen.blit(self.drill_img, [0, 0])

class Mining(state_machine.State):
    """Mining task.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)

    def startup(self):
        self.next = random.choice(self.task_list)
        self.count = 0
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.mine_img = tools.images['mining-1']
        self.score_check(self.score)

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
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, timer_text, 40, self.screen_width/2, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, timer_text, 40, self.screen_width/2, 0, screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, score_text, 40, self.screen_width-150, 0, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, score_text, 40, self.screen_width-150, 0, screen)
        tools.draw_progress_bar(self.screen_width-100, self.screen_height/4, self.count*20, screen)
        self.count_check(self.count, timer)

    def draw(self, screen):
        screen.blit(self.mine_img, [0, 0])

class Loss(state_machine.State):
    """Loss state.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)
        self.next = 'menu'

    def startup(self):
        self.loss_img = tools.images['game-over']
        tools.play_music(tools.sounds['piano-lofi-rain'])
        self.score_text = 'Final Score: ' + str(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True

    def update(self, screen, dt):
        self.loss_img = tools.render_image(self.loss_img, self.screen_size, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, self.score_text, 100, self.screen_width/2, self.screen_height/2.5, screen)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.loss_img, [0, 0])

class Win(state_machine.State):
    """Win state.
    """

    def __init__(self):
        state_machine.State.__init__(self)
        self.__dict__.update(state_machine.settings)
        self.next = 'menu'

    def startup(self):
        self.win_img = tools.images['winner']
        tools.play_music(tools.sounds['future-grid'])

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