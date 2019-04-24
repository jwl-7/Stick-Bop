import pygame
import sys
from . import state_machine
from . import states

def main():
    """Initialize pygame, state machine, and runs the main game loop."""
    pygame.init()
    game = state_machine.StateController(**state_machine.settings)
    state_dict = {
            'loading': states.Loading(),
            'menu': states.Menu(),
            'start': states.Start(),
            'loss': states.Loss(),
            'win': states.Win(),
            'drilling': states.Drilling(),
            'mining': states.Mining(),
            'woodchopping': states.Woodchopping()
        }
    game.setup_states(state_dict, 'loading')
    game.game_loop()
    pygame.quit()
    sys.exit()