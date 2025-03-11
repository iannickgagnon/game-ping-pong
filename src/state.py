
# Standard library imports
from enum import Enum


class State(Enum):
    """
    State is an enumeration that represents the different states of the game.

    Attributes:
        MENU (int): Represents the menu state of the game.
        PLAY (int): Represents the play state of the game.
        GAME_OVER (int): Represents the game over state of the game.
    """
    MENU = 1
    PLAY = 2
    GAME_OVER = 3
