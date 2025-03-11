
# Pygame imports
from pgzero.actor import Actor

# Local application imports
from src.constants import (HALF_HEIGHT_PX, 
                           HALF_WIDTH_PX, 
                           MAX_AI_SPEED)

class Bat(Actor):

    def __init__(self, player, game, move_func=None):
        x = 40 if player == 0 else 760
        y = HALF_HEIGHT_PX
        super().__init__("blank", (x, y))

        self.player = player
        self.score = 0
        self.game = game

        # move_func is a function we may or may not have been passed by the code which created this object. If this bat
        # is meant to be player controlled, move_func will be a function that when called, returns a number indicating
        # the direction and speed in which the bat should move, based on the keys the player is currently pressing.
        # If move_func is None, this indicates that this bat should instead be controlled by the AI method.
        if move_func != None:
            self.move_func = move_func
        else:
            self.move_func = self.ai

        # Each bat has a timer which starts at zero and counts down by one every frame. When a player concedes a point,
        # their timer is set to 20, which causes the bat to display a different animation frame. It is also used to
        # decide when to create a new ball in the centre of the screen - see comments in Game.update for more on this.
        # Finally, it is used in Game.draw to determine when to display a visual effect over the top of the background
        self.timer = 0

    def update(self):
        self.timer -= 1

        # Our movement function tells us how much to move on the Y axis
        y_movement = self.move_func()

        # Apply y_movement to y position, ensuring bat does not go through the side walls
        self.y = min(400, max(80, self.y + y_movement))

        # Choose the appropriate sprite. There are 3 sprites per player - e.g. bat00 is the left-hand player's
        # standard bat sprite, bat01 is the sprite to use when the ball has just bounced off the bat, and bat02
        # is the sprite to use when the bat has just missed the ball and the ball has gone out of bounds.
        # bat10, 11 and 12 are the equivalents for the right-hand player

        frame = 0
        if self.timer > 0:
            if self.game.ball.is_out():
                frame = 2
            else:
                frame = 1

        self.image = "bat" + str(self.player) + str(frame)

    def ai(self):
        
        # Returns a number indicating how the computer player will move - e.g. 4 means it will move 4 pixels down
        # the screen.

        # To decide where we want to go, we first check to see how far we are from the ball.
        x_distance = abs(self.game.ball.x - self.x)

        # If the ball is far away, we move towards the centre of the screen (HALF_HEIGHT), on the basis that we don't
        # yet know whether the ball will be in the top or bottom half of the screen when it reaches our position on
        # the X axis. By waiting at a central position, we're as ready as it's possible to be for all eventualities.
        target_y_1 = HALF_HEIGHT_PX

        # If the ball is close, we want to move towards its position on the Y axis. We also apply a small offset which
        # is randomly generated each time the ball bounces. This is to make the computer player slightly less robotic
        # - a human player wouldn't be able to hit the ball right in the centre of the bat each time.
        target_y_2 = self.game.ball.y + self.game.ai_offset

        # The final step is to work out the actual Y position we want to move towards. We use what's called a weighted
        # average - taking the average of the two target Y positions we've previously calculated, but shifting the
        # balance towards one or the other depending on how far away the ball is. If the ball is more than 400 pixels
        # (half the screen width) away on the X axis, our target will be half the screen height (target_y_1). If the
        # ball is at the same position as us on the X axis, our target will be target_y_2. If it's 200 pixels away,
        # we'll aim for halfway between target_y_1 and target_y_2. This reflects the idea that as the ball gets closer,
        # we have a better idea of where it's going to end up.
        weight1 = min(1, x_distance / HALF_WIDTH_PX)
        weight2 = 1 - weight1

        target_y = (weight1 * target_y_1) + (weight2 * target_y_2)

        # Subtract target_y from our current Y position, then make sure we can't move any further than MAX_AI_SPEED
        # each frame
        return min(MAX_AI_SPEED, max(-MAX_AI_SPEED, target_y - self.y))