"""Finite State Machine

This module contains the game state controller and prototype state class.
"""


import pygame

from . import tools


TITLE = 'Stick Bop!'
WINDOW_SIZE = (1000, 800)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FPS = 60


class StateController:
    """Controls and sets up the game settings, game states, and main game loop.

    Attributes:
        done (bool): State completion status.
        screen (obj): Initializes display surface.
        caption (obj): Sets the window title.
        clock (obj): Initializes clock object to help track time.
        states (dict): The various game states.
    """

    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        tools.change_icon('helmet-icon.png')
        self.caption = pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.states = {}

    def setup_states(self, state_dict, start_state):
        """Sets the initial state.

        Args:
            state_dict (dict): Holds a list of all states and their respective class instances.
            start_state (str): The name of the first state to be used.
        """
        self.states = state_dict
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


class State(object):
    """Prototype class for all game states to inherit from.

    Attributes:
        score (int): Holds the game score.
        count (int): Represents the progress of task completion.
        task_list (list): List of game states. Used for randomly shuffling tasks.
        done (bool): State completion status.
        quit (bool): State exit status.
        next (none): Holds the value of the next state.
        current (none): Holds the value of the current state.
    """
    score = 0
    count = 0
    task_list = [
        'drilling',
        'mining',
        'woodchopping',
        'flagraising',
        'hammering',
        'tirepumping'
        ]

    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.current = None
        self.screen_size = WINDOW_SIZE
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT

    def music_check(self, score):
        """Checks for when to speed up music.

        Args:
            score (int): Game score.
        """
        if score == 0:
            tools.play_music(tools.sounds['neon-runner'])
        elif score == 25:
            tools.play_music(tools.sounds['neon-runner-x125'])
        elif score == 50:
            tools.play_music(tools.sounds['neon-runner-x150'])
        elif score == 75:
            tools.play_music(tools.sounds['neon-runner-x175'])

    def count_check(self, count, timer):
        """Checks for task completion / fail.

        Args:
            count (int): Represents the progress of task completion.
            timer (int): Rounded time in seconds elapsed since task started.
        """
        if count >= 5 and timer > 0:
            State.score += 1
            tools.play_sound(tools.sounds['task-done'])
            self.next = 'taskdone'
            self.done = True
        elif timer <= 0:
            self.next = 'loss'
            self.done = True

    def timer_check(self, score):
        """Checks for what the timer should start at for the task.

        Args:
            score (int): Game score.
        """
        if score >= 0 and score < 25:
            start_time = 5
        elif score >= 25 and score < 50:
            start_time = 4.5
        elif score >= 50 and score < 75:
            start_time = 4
        elif score >= 75:
            start_time = 3.5
        return start_time
