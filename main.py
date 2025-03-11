# Pygame imports
import pgzrun
import pygame

# Local application imports
from src.utilities import check_python_pygame_versions
from src.state import State
from src.game import Game

# Local application constants
from src.constants import PLAYER_SPEED

# Pygame Zero builtins will be automatically available
# Do not import screen, keyboard - they are builtins
from pgzero.builtins import sounds, music

# Declare global game variables
global state
global game 
global num_players
global space_down

# Check Python and Pygame versions
check_python_pygame_versions()

def p1_controls():
    move = 0
    if keyboard.z or keyboard.down:
        move = PLAYER_SPEED
    elif keyboard.a or keyboard.up:
        move = -PLAYER_SPEED
    return move

def p2_controls():
    move = 0
    if keyboard.m:
        move = PLAYER_SPEED
    elif keyboard.k:
        move = -PLAYER_SPEED
    return move

# Pygame Zero calls the update and draw functions each frame
def update():
    
    global state
    global num_players
    global game
    global space_down

    # Initialize game with screen on first run if not already initialized
    if game.screen is None:
        game.screen = screen

    # Work out whether the space key has just been pressed - i.e. in the previous frame it wasn't down,
    # and in this frame it is.
    space_pressed = False
    if keyboard.space and not space_down:
        space_pressed = True
    space_down = keyboard.space

    if state == State.MENU:
        if space_pressed:
            # Switch to play state, and create a new Game object, passing it the controls function for
            # player 1, and if we're in 2 player mode, the controls function for player 2 (otherwise the
            # 'None' value indicating this player should be computer-controlled)
            state = State.PLAY
            controls = [p1_controls]
            controls.append(p2_controls if num_players == 2 else None)
            game = Game(screen, controls)
        else:
            # Detect up/down keys
            if num_players == 2 and keyboard.up:
                sounds.up.play()
                num_players = 1
            elif num_players == 1 and keyboard.down:
                sounds.down.play()
                num_players = 2

            # Update the 'attract mode' game in the background (two AIs playing each other)
            game.update()

    elif state == State.PLAY:
        # Has anyone won?
        if max(game.bats[0].score, game.bats[1].score) > 9:
            state = State.GAME_OVER
        else:
            game.update()

    elif state == State.GAME_OVER:
        if space_pressed:
            # Reset to menu state
            state = State.MENU
            num_players = 1

            # Create a new Game object, without any players
            game = Game()

def draw():
    game.draw()

    if state == State.MENU:
        menu_image = "menu" + str(num_players - 1)
        screen.blit(menu_image, (0,0))

    elif state == State.GAME_OVER:
        screen.blit("over", (0,0))


# The mixer allows us to play sounds and music
try:

    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)

    music.play("theme")
    music.set_volume(0.3)

except:
    # If an error occurs (e.g. no sound device), just ignore it
    pass


# Set the initial game state at the main menu
state = State.MENU

# Create a new Game object, without any players - don't pass screen yet
game = Game()

# The initial number of players is set to 1
num_players = 1

# The space key is not pressed at the start of the game
space_down = False

# Start Pygame Zero
pgzrun.go()
