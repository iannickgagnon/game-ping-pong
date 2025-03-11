# Standard library imports
import random

# Local application imports
from src.bat import Bat
from src.ball import Ball

# Local application constants
from src.constants import WIDTH_PX

class Game:
    def __init__(self, screen=None, controls=(None, None)):
        # Create a list of two bats, giving each a player number and a function to use to receive
        # control inputs (or the value None if this is intended to be an AI player)
        self.bats = [Bat(0, self, controls[0]), Bat(1, self, controls[1])]

        # Create a ball object
        self.ball = Ball(-1, self)

        # Create an empty list which will later store the details of currently playing impact
        # animations - these are displayed for a short time every time the ball bounces
        self.impacts = []

        # Add an offset to the AI player's target Y position, so it won't aim to hit the ball exactly
        # in the centre of the bat
        self.ai_offset = 0

        self.screen = screen

    def update(self):
        # Update all active objects
        for obj in self.bats + [self.ball] + self.impacts:
            obj.update()

        # Remove any expired impact effects from the list. We go through the list backwards, starting from the last
        # element, and delete any elements those time attribute has reached 10. We go backwards through the list
        # instead of forwards to avoid a number of issues which occur in that scenario. In the next chapter we will
        # look at an alternative technique for removing items from a list, using list comprehensions.
        for i in range(len(self.impacts) - 1, -1, -1):
            if self.impacts[i].time >= 10:
                del self.impacts[i]

        # Has ball gone off the left or right edge of the screen?
        if self.ball.is_out():
            # Work out which player gained a point, based on whether the ball
            # was on the left or right-hand side of the screen
            scoring_player = 1 if self.ball.x < WIDTH_PX // 2 else 0
            losing_player = 1 - scoring_player

            # We use the timer of the player who has just conceded a point to decide when to create a new ball in the
            # centre of the level. This timer starts at zero at the beginning of the game and counts down by one every
            # frame. Therefore, on the frame where the ball first goes off the screen, the timer will be less than zero.
            # We set it to 20, which means that this player's bat will display a different animation frame for 20
            # frames, and a new ball will be created after 20 frames
            if self.bats[losing_player].timer < 0:
                self.bats[scoring_player].score += 1

                self.play_sound("score_goal", 1)

                self.bats[losing_player].timer = 20

            elif self.bats[losing_player].timer == 0:
                # After 20 frames, create a new ball, heading in the direction of the player who just missed the ball
                direction = -1 if losing_player == 0 else 1
                self.ball = Ball(direction, self)

    def draw(self):
        if not self.screen:
            return

        # Draw background
        self.screen.blit("table", (0,0))

        # Draw 'just scored' effects, if required
        for p in (0,1):
            if self.bats[p].timer > 0 and self.ball.is_out():
                self.screen.blit("effect" + str(p), (0,0))

        # Draw bats, ball and impact effects - in that order. Square brackets are needed around the ball because
        # it's just an object, whereas the other two are lists - and you can't directly join an object onto a
        # list without first putting it in a list
        for obj in self.bats + [self.ball] + self.impacts:
            obj.draw()

        # Display scores - outer loop goes through each player
        for p in (0,1):
            # Convert score into a string of 2 digits (e.g. "05") so we can later get the individual digits
            score = "{0:02d}".format(self.bats[p].score)
            # Inner loop goes through each digit
            for i in (0,1):
                # Digit sprites are numbered 00 to 29, where the first digit is the colour (0 = grey,
                # 1 = blue, 2 = green) and the second digit is the digit itself
                # Colour is usually grey but turns red or green (depending on player number) when a
                # point has just been scored
                colour = "0"
                other_p = 1 - p
                if self.bats[other_p].timer > 0 and self.ball.is_out():
                    colour = "2" if p == 0  else "1"
                image = "digit" + colour + str(score[i])
                self.screen.blit(image, (255 + (160 * p) + (i * 55), 46))

    def play_sound(self, name, count=1):
        # Some sounds have multiple varieties. If count > 1, we'll randomly choose one from those
        # We don't play any in-game sound effects if player 0 is an AI player - as this means we're on the menu
        if self.bats[0].move_func != self.bats[0].ai:
            # Pygame Zero allows you to write things like 'sounds.explosion.play()'
            # This automatically loads and plays a file named 'explosion.wav' (or .ogg) from the sounds folder (if
            # such a file exists)
            # But what if you have files named 'explosion0.ogg' to 'explosion5.ogg' and want to randomly choose
            # one of them to play? You can generate a string such as 'explosion3', but to use such a string
            # to access an attribute of Pygame Zero's sounds object, we must use Python's built-in function getattr
            try:
                getattr(sounds, name + str(random.randint(0, count - 1))).play()
            except:
                pass