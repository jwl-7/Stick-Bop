""" Game States

This module contains all the game states
for use with the finite state machine.
"""


import random
import os

import pygame

from . import state_machine
from . import tools


class Loading(state_machine.State):
    """Displays loading image. Loads all assets including fonts, images, and sounds."""

    def __init__(self):
        state_machine.State.__init__(self)
        self.next = 'menu'
        self.load = True
        self.start_time = pygame.time.get_ticks()
        self.load_img = pygame.image.load(os.path.join(tools.IMG_DIR, 'loading.png')).convert()

    def load_assets(self):
        if self.load:
            tools.images = tools.load_images(tools.IMG_DIR)
            tools.sounds = tools.load_sounds(tools.SND_DIR)
            tools.fonts = tools.load_fonts(tools.FNT_DIR)
            self.load = False

    def startup(self):
        pass

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        self.load_img = tools.render_image(self.load_img, self.screen_size, screen)
        self.draw(screen)
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if time_elapsed >= 200:
            self.load_assets()
        if not self.load:
            self.done = True

    def draw(self, screen):
        screen.blit(self.load_img, [0, 0])


class Menu(state_machine.State):
    """Displays main menu. Allows user to start or quit game."""

    def __init__(self):
        state_machine.State.__init__(self)
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


class Start(state_machine.State):
    """Displays ready, set, GO! message with sound and starts the game."""

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        state_machine.State.score = 0
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


class Taskdone(state_machine.State):
    """Sets the next state to a random task and then switches to it after 400ms."""

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.score_check(self.score)
        self.start_time = pygame.time.get_ticks()

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if time_elapsed >= 400:
            self.done = True

    def draw(self, screen):
        pass

    def score_check(self, score):
        """Checks the score to determine the next state.

        Args:
            score (int): Game score.
        """
        if score == 24:
            self.next = 'excalibur1'
        elif score == 49:
            self.next = 'excalibur2'
        elif score == 74:
            self.next = 'excalibur3'
        elif score == 99:
            self.next = 'excalibur4'
        elif score == 100:
            self.next = 'win'
        else:
            self.next = random.choice(self.task_list)


class Woodchopping(state_machine.State):
    """Woodchopping task.

    Key Sequence:
        Right -> Left (5x).
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.wood_img = tools.images['woodchopping-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if self.right_was_pressed and not self.right_pressed:
                self.wood_img = tools.images['woodchopping-1']
                self.right_was_pressed = False
                if self.count == 4:
                    self.wood_img = tools.images['woodchopping-3']
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if not self.right_was_pressed and not self.left_pressed:
                self.wood_img = tools.images['woodchopping-2']
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
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

    Key Sequence:
        Space (5x).
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.drill_img = tools.images['drilling-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.count == 0:
                self.drill_img = tools.images['drilling-2']
            elif self.count == 1:
                self.drill_img = tools.images['drilling-4']
            elif self.count == 2:
                self.drill_img = tools.images['drilling-6']
            elif self.count == 3:
                self.drill_img = tools.images['drilling-8']
            elif self.count == 4:
                self.drill_img = tools.images['drilling-10']
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self.count == 0:
                self.drill_img = tools.images['drilling-3']
            elif self.count == 1:
                self.drill_img = tools.images['drilling-5']
            elif self.count == 2:
                self.drill_img = tools.images['drilling-7']
            elif self.count == 3:
                self.drill_img = tools.images['drilling-9']
            elif self.count == 4:
                self.drill_img = tools.images['drilling-11']
            self.count += 1

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

    Key Sequence:
        Right -> Left (5x).
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.left_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.mine_img = tools.images['mining-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if self.right_was_pressed and not self.right_pressed:
                if self.count == 0:
                    self.mine_img = tools.images['mining-3']
                elif self.count == 1:
                    self.mine_img = tools.images['mining-5']
                elif self.count == 2:
                    self.mine_img = tools.images['mining-7']
                elif self.count == 3:
                    self.mine_img = tools.images['mining-9']
                elif self.count == 4:
                    self.mine_img = tools.images['mining-11']
                self.right_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if not self.right_was_pressed and not self.left_pressed:
                if self.count == 0:
                    self.mine_img = tools.images['mining-2']
                elif self.count == 1:
                    self.mine_img = tools.images['mining-4']
                elif self.count == 2:
                    self.mine_img = tools.images['mining-6']
                elif self.count == 3:
                    self.mine_img = tools.images['mining-8']
                elif self.count == 4:
                    self.mine_img = tools.images['mining-10']
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
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


class Flagraising(state_machine.State):
    """Flagraising task.

    Key Sequence:
        Down -> Up (5x).
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.up_pressed = False
        self.down_pressed = False
        self.down_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.flag_img = tools.images['flagraising-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up_pressed = True
            if self.down_was_pressed and not self.down_pressed:
                if self.count == 0:
                    self.flag_img = tools.images['flagraising-3']
                elif self.count == 1:
                    self.flag_img = tools.images['flagraising-5']
                elif self.count == 2:
                    self.flag_img = tools.images['flagraising-7']
                elif self.count == 3:
                    self.flag_img = tools.images['flagraising-9']
                elif self.count == 4:
                    self.flag_img = tools.images['flagraising-11']
                self.down_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            if not self.down_was_pressed and not self.up_pressed:
                if self.count == 0:
                    self.flag_img = tools.images['flagraising-2']
                elif self.count == 1:
                    self.flag_img = tools.images['flagraising-4']
                elif self.count == 2:
                    self.flag_img = tools.images['flagraising-6']
                elif self.count == 3:
                    self.flag_img = tools.images['flagraising-8']
                elif self.count == 4:
                    self.flag_img = tools.images['flagraising-10']
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            self.up_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            if self.down_pressed:
                self.down_pressed = False
                self.down_was_pressed = True

    def update(self, screen, dt):
        self.flag_img = tools.render_image(self.flag_img, self.screen_size, screen)
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
        screen.blit(self.flag_img, [0, 0])


class Hammering(state_machine.State):
    """Hammering task.

    Key Sequence:
        Space (10x).
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.hammer_img = tools.images['hammering-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.count == 0:
                self.hammer_img = tools.images['hammering-2']
            elif self.count == 0.5:
                self.hammer_img = tools.images['hammering-4']
            elif self.count == 1:
                self.hammer_img = tools.images['hammering-6']
            elif self.count == 1.5:
                self.hammer_img = tools.images['hammering-8']
            elif self.count == 2:
                self.hammer_img = tools.images['hammering-10']
            elif self.count == 2.5:
                self.hammer_img = tools.images['hammering-12']
            elif self.count == 3:
                self.hammer_img = tools.images['hammering-14']
            elif self.count == 3.5:
                self.hammer_img = tools.images['hammering-16']
            elif self.count == 4:
                self.hammer_img = tools.images['hammering-18']
            elif self.count == 4.5:
                self.hammer_img = tools.images['hammering-20']
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self.count == 0:
                self.hammer_img = tools.images['hammering-3']
            elif self.count == 0.5:
                self.hammer_img = tools.images['hammering-5']
            elif self.count == 1:
                self.hammer_img = tools.images['hammering-7']
            elif self.count == 1.5:
                self.hammer_img = tools.images['hammering-9']
            elif self.count == 2:
                self.hammer_img = tools.images['hammering-11']
            elif self.count == 2.5:
                self.hammer_img = tools.images['hammering-13']
            elif self.count == 3:
                self.hammer_img = tools.images['hammering-15']
            elif self.count == 3.5:
                self.hammer_img = tools.images['hammering-17']
            elif self.count == 4:
                self.hammer_img = tools.images['hammering-19']
            elif self.count == 4.5:
                self.hammer_img = tools.images['hammering-21']
            self.count += 0.5

    def update(self, screen, dt):
        self.hammer_img = tools.render_image(self.hammer_img, self.screen_size, screen)
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
        screen.blit(self.hammer_img, [0, 0])


class Tirepumping(state_machine.State):
    """Tirepumping task.

    Key Sequence:
        Down -> Up (5x).
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.up_pressed = False
        self.down_pressed = False
        self.down_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.tire_img = tools.images['tirepumping-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up_pressed = True
            if self.down_was_pressed and not self.down_pressed:
                if self.count == 0:
                    self.tire_img = tools.images['tirepumping-3']
                elif self.count == 1:
                    self.tire_img = tools.images['tirepumping-5']
                elif self.count == 2:
                    self.tire_img = tools.images['tirepumping-7']
                elif self.count == 3:
                    self.tire_img = tools.images['tirepumping-9']
                elif self.count == 4:
                    self.tire_img = tools.images['tirepumping-11']
                self.down_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            if not self.down_was_pressed and not self.up_pressed:
                if self.count == 0:
                    self.tire_img = tools.images['tirepumping-2']
                elif self.count == 1:
                    self.tire_img = tools.images['tirepumping-4']
                elif self.count == 2:
                    self.tire_img = tools.images['tirepumping-6']
                elif self.count == 3:
                    self.tire_img = tools.images['tirepumping-8']
                elif self.count == 4:
                    self.tire_img = tools.images['tirepumping-10']
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            self.up_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            if self.down_pressed:
                self.down_pressed = False
                self.down_was_pressed = True

    def update(self, screen, dt):
        self.tire_img = tools.render_image(self.tire_img, self.screen_size, screen)
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
        screen.blit(self.tire_img, [0, 0])


class Excalibur1(state_machine.State):
    """Excalibur1 task.

    Key Sequence:
        Up -> Up, Down -> Down, Left -> Right, Left -> Right, Space -> Space.
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.up_pressed = False
        self.up_was_pressed = False
        self.down_pressed = False
        self.down_was_pressed = False
        self.left_pressed = False
        self.left_was_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.space_pressed = False
        self.space_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.excalibur1_img = tools.images['excalibur-1-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up_pressed = True
            if not self.up_was_pressed and self.count == 0:
                self.excalibur1_img = tools.images['excalibur-1-2']
            elif self.up_was_pressed and self.count == 0:
                self.excalibur1_img = tools.images['excalibur-1-3']
                self.up_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            if not self.down_was_pressed and self.count == 1:
                self.excalibur1_img = tools.images['excalibur-1-4']
            elif self.down_was_pressed and self.count == 1:
                self.excalibur1_img = tools.images['excalibur-1-5']
                self.down_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if not self.left_was_pressed and self.count == 2:
                self.excalibur1_img = tools.images['excalibur-1-6']
            elif not self.left_was_pressed and self.count == 3:
                self.excalibur1_img = tools.images['excalibur-1-8']
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if self.left_was_pressed and self.count == 2:
                self.excalibur1_img = tools.images['excalibur-1-7']
                self.left_was_pressed = False
                self.count += 1
            elif self.left_was_pressed and self.count == 3:
                self.excalibur1_img = tools.images['excalibur-1-9']
                self.left_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.space_pressed = True
            if not self.space_was_pressed and self.count == 4:
                self.excalibur1_img = tools.images['excalibur-1-10']
            elif self.space_was_pressed and self.count == 4:
                self.excalibur1_img = tools.images['excalibur-1-11']
                self.space_was_pressed = False
                self.count += 1
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            if self.up_pressed:
                if self.count == 0:
                    self.up_was_pressed = True
                self.up_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            if self.down_pressed:
                if self.count == 1:
                    self.down_was_pressed = True
                self.down_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            if self.left_pressed:
                if self.count == 2 or self.count == 3:
                    self.left_was_pressed = True
                self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                if self.count == 2 or self.count == 3:
                    self.right_was_pressed = True
                self.right_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self.space_pressed:
                if self.count == 4:
                    self.space_was_pressed = True
                self.space_pressed = False

    def update(self, screen, dt):
        self.excalibur1_img = tools.render_image(self.excalibur1_img, self.screen_size, screen)
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
        screen.blit(self.excalibur1_img, [0, 0])


class Excalibur2(state_machine.State):
    """Excalibur2 task.

    Key Sequence:
        Up -> Up, Down -> Down, Left -> Right, Left -> Right, Space -> Space.
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.up_pressed = False
        self.up_was_pressed = False
        self.down_pressed = False
        self.down_was_pressed = False
        self.left_pressed = False
        self.left_was_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.space_pressed = False
        self.space_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.excalibur2_img = tools.images['excalibur-2-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up_pressed = True
            if not self.up_was_pressed and self.count == 0:
                self.excalibur2_img = tools.images['excalibur-2-2']
            elif self.up_was_pressed and self.count == 0:
                self.excalibur2_img = tools.images['excalibur-2-3']
                self.up_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            if not self.down_was_pressed and self.count == 1:
                self.excalibur2_img = tools.images['excalibur-2-4']
            elif self.down_was_pressed and self.count == 1:
                self.excalibur2_img = tools.images['excalibur-2-5']
                self.down_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if not self.left_was_pressed and self.count == 2:
                self.excalibur2_img = tools.images['excalibur-2-6']
            elif not self.left_was_pressed and self.count == 3:
                self.excalibur2_img = tools.images['excalibur-2-8']
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if self.left_was_pressed and self.count == 2:
                self.excalibur2_img = tools.images['excalibur-2-7']
                self.left_was_pressed = False
                self.count += 1
            elif self.left_was_pressed and self.count == 3:
                self.excalibur2_img = tools.images['excalibur-2-9']
                self.left_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.space_pressed = True
            if not self.space_was_pressed and self.count == 4:
                self.excalibur2_img = tools.images['excalibur-2-10']
            elif self.space_was_pressed and self.count == 4:
                self.excalibur2_img = tools.images['excalibur-2-11']
                self.space_was_pressed = False
                self.count += 1
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            if self.up_pressed:
                if self.count == 0:
                    self.up_was_pressed = True
                self.up_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            if self.down_pressed:
                if self.count == 1:
                    self.down_was_pressed = True
                self.down_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            if self.left_pressed:
                if self.count == 2 or self.count == 3:
                    self.left_was_pressed = True
                self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                if self.count == 2 or self.count == 3:
                    self.right_was_pressed = True
                self.right_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self.space_pressed:
                if self.count == 4:
                    self.space_was_pressed = True
                self.space_pressed = False

    def update(self, screen, dt):
        self.excalibur2_img = tools.render_image(self.excalibur2_img, self.screen_size, screen)
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
        screen.blit(self.excalibur2_img, [0, 0])


class Excalibur3(state_machine.State):
    """Excalibur3 task.

    Key Sequence:
        Up -> Up, Down -> Down, Left -> Right, Left -> Right, Space -> Space.
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.up_pressed = False
        self.up_was_pressed = False
        self.down_pressed = False
        self.down_was_pressed = False
        self.left_pressed = False
        self.left_was_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.space_pressed = False
        self.space_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.excalibur3_img = tools.images['excalibur-3-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up_pressed = True
            if not self.up_was_pressed and self.count == 0:
                self.excalibur3_img = tools.images['excalibur-3-2']
            elif self.up_was_pressed and self.count == 0:
                self.excalibur3_img = tools.images['excalibur-3-3']
                self.up_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            if not self.down_was_pressed and self.count == 1:
                self.excalibur3_img = tools.images['excalibur-3-4']
            elif self.down_was_pressed and self.count == 1:
                self.excalibur3_img = tools.images['excalibur-3-5']
                self.down_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if not self.left_was_pressed and self.count == 2:
                self.excalibur3_img = tools.images['excalibur-3-6']
            elif not self.left_was_pressed and self.count == 3:
                self.excalibur3_img = tools.images['excalibur-3-8']
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if self.left_was_pressed and self.count == 2:
                self.excalibur3_img = tools.images['excalibur-3-7']
                self.left_was_pressed = False
                self.count += 1
            elif self.left_was_pressed and self.count == 3:
                self.excalibur3_img = tools.images['excalibur-3-9']
                self.left_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.space_pressed = True
            if not self.space_was_pressed and self.count == 4:
                self.excalibur3_img = tools.images['excalibur-3-10']
            elif self.space_was_pressed and self.count == 4:
                self.excalibur3_img = tools.images['excalibur-3-11']
                self.space_was_pressed = False
                self.count += 1
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            if self.up_pressed:
                if self.count == 0:
                    self.up_was_pressed = True
                self.up_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            if self.down_pressed:
                if self.count == 1:
                    self.down_was_pressed = True
                self.down_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            if self.left_pressed:
                if self.count == 2 or self.count == 3:
                    self.left_was_pressed = True
                self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                if self.count == 2 or self.count == 3:
                    self.right_was_pressed = True
                self.right_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self.space_pressed:
                if self.count == 4:
                    self.space_was_pressed = True
                self.space_pressed = False

    def update(self, screen, dt):
        self.excalibur3_img = tools.render_image(self.excalibur3_img, self.screen_size, screen)
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
        screen.blit(self.excalibur3_img, [0, 0])


class Excalibur4(state_machine.State):
    """Excalibur4 task.

    Key Sequence:
        Up -> Up, Down -> Down, Left -> Right, Left -> Right, Space -> Space.
    """

    def __init__(self):
        state_machine.State.__init__(self)

    def startup(self):
        self.count = 0
        self.up_pressed = False
        self.up_was_pressed = False
        self.down_pressed = False
        self.down_was_pressed = False
        self.left_pressed = False
        self.left_was_pressed = False
        self.right_pressed = False
        self.right_was_pressed = False
        self.space_pressed = False
        self.space_was_pressed = False
        self.start_time = pygame.time.get_ticks()
        self.timer_start = self.timer_check(self.score)
        self.excalibur4_img = tools.images['excalibur-4-1']
        self.music_check(self.score)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.up_pressed = True
            if not self.up_was_pressed and self.count == 0:
                self.excalibur4_img = tools.images['excalibur-4-2']
            elif self.up_was_pressed and self.count == 0:
                self.excalibur4_img = tools.images['excalibur-4-3']
                self.up_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.down_pressed = True
            if not self.down_was_pressed and self.count == 1:
                self.excalibur4_img = tools.images['excalibur-4-4']
            elif self.down_was_pressed and self.count == 1:
                self.excalibur4_img = tools.images['excalibur-4-5']
                self.down_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.left_pressed = True
            if not self.left_was_pressed and self.count == 2:
                self.excalibur4_img = tools.images['excalibur-4-6']
            elif not self.left_was_pressed and self.count == 3:
                self.excalibur4_img = tools.images['excalibur-4-8']
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.right_pressed = True
            if self.left_was_pressed and self.count == 2:
                self.excalibur4_img = tools.images['excalibur-4-7']
                self.left_was_pressed = False
                self.count += 1
            elif self.left_was_pressed and self.count == 3:
                self.excalibur4_img = tools.images['excalibur-4-9']
                self.left_was_pressed = False
                self.count += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.space_pressed = True
            if not self.space_was_pressed and self.count == 4:
                self.excalibur4_img = tools.images['excalibur-4-10']
            elif self.space_was_pressed and self.count == 4:
                self.excalibur4_img = tools.images['excalibur-4-11']
                self.space_was_pressed = False
                self.count += 1
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            if self.up_pressed:
                if self.count == 0:
                    self.up_was_pressed = True
                self.up_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            if self.down_pressed:
                if self.count == 1:
                    self.down_was_pressed = True
                self.down_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            if self.left_pressed:
                if self.count == 2 or self.count == 3:
                    self.left_was_pressed = True
                self.left_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            if self.right_pressed:
                if self.count == 2 or self.count == 3:
                    self.right_was_pressed = True
                self.right_pressed = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if self.space_pressed:
                if self.count == 4:
                    self.space_was_pressed = True
                self.space_pressed = False

    def update(self, screen, dt):
        self.excalibur4_img = tools.render_image(self.excalibur4_img, self.screen_size, screen)
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
        screen.blit(self.excalibur4_img, [0, 0])


class Loss(state_machine.State):
    """Game loss."""

    def __init__(self):
        state_machine.State.__init__(self)
        self.next = 'menu'

    def startup(self):
        self.loss_img = tools.images['game-over']
        self.score_text = 'Final Score: ' + str(self.score)
        tools.play_music(tools.sounds['piano-lofi-rain'])

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.done = True

    def update(self, screen, dt):
        self.loss_img = tools.render_image(self.loss_img, self.screen_size, screen)
        self.draw(screen)
        tools.clear_text(tools.fonts['OpenSans-Regular'], tools.WHITE, self.score_text, 100, self.screen_width/2, self.screen_height/2.5, screen)
        tools.render_text(tools.fonts['OpenSans-Regular'], tools.BLACK, self.score_text, 100, self.screen_width/2, self.screen_height/2.5, screen)

    def draw(self, screen):
        screen.blit(self.loss_img, [0, 0])


class Win(state_machine.State):
    """Game won."""

    def __init__(self):
        state_machine.State.__init__(self)
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
