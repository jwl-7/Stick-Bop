import pygame
import sys
from . import state_machine
from . import states

def main():
    """Initialize pygame, state machine, and run the main game loop."""
    pygame.init()
    game = state_machine.StateController(**state_machine.settings)
    state_dict = {
            'loading': states.Loading(),
            'menu': states.Menu(),
            'start': states.Start(),
            'loss': states.Loss(),
            'win': states.Win(),
            'taskdone': states.Taskdone(),
            'drilling': states.Drilling(),
            'mining': states.Mining(),
            'woodchopping': states.Woodchopping(),
            'flagraising': states.Flagraising(),
            'hammering': states.Hammering(),
            'tirepumping': states.Tirepumping(),
            'excalibur1': states.Excalibur1(),
            'excalibur2': states.Excalibur2(),
            'excalibur3': states.Excalibur3(),
            'excalibur4': states.Excalibur4()
        }
    game.setup_states(state_dict, 'loading')
    game.game_loop()
    pygame.quit()
    sys.exit()