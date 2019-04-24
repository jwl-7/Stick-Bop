import pygame
from . import tools

# pygame display settings dictionary
settings = {
    'screen_size': (900, 700),
    'screen_width': 900,
    'screen_height': 700,
    'screen_max_width': 1920,
    'screen_max_height': 1080,
    'fps': 60,
    'title': 'Stick Bop!'  
}

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
    task_list = ['drilling', 'mining', 'woodchopping']

    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.current = None

    def score_check(self, score):
        """Checks for when to speed up music and win state.

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
        elif score == 100:
            self.next = 'win'
            self.done = True

    def count_check(self, count, timer):
        """Checks for task completion / fail.
        
        Args:
            count (int): Represents the progress of task completion.
            timer (int): Rounded time in seconds elapsed since task started.
        """
        if count >= 5 and timer > 0:
            State.score += 1
            tools.play_sound(tools.sounds['task-done'])
            self.done = True
        elif timer <= 0:
            self.next = 'loss'
            self.done = True

    def timer_check(self, score):
        """Checks for what the timer should start at for the task.

        Args:
            score (int): Game score.
        """
        if score >= 0:
            start_time = 5
        elif score >= 25:
            start_time = 4.5
        elif score >= 50:
            start_time = 4
        elif score >= 75:
            start_time = 3.5
        return start_time