import pygame
from . import tools

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
        self.states = {}
        '''
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
        '''
    
    def setup_states(self, states, start_state):
        """Sets the initial state."""
        self.states = states
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