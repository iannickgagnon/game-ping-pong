# Pygame imports
from pgzero.actor import Actor


class Impact(Actor):
    """
    A class to represent an impact effect in the game when a ball bounces.

    This class inherits from the Actor class and is used to create and update
    impact effects at a given position. The impact effect changes its sprite
    every 2 frames and is removed from the game after 10 frames.

    Attributes:
        time (int): A counter to track the number of frames since the impact was created.
    """

    def __init__(self, pos):
        """
        Initializes the Impact instance with a position and sets the initial time to 0.

        Args:
            pos (tuple): The (x, y) position where the impact effect should be created.
        """
        super().__init__("blank", pos)
        self.time = 0

    def update(self):
        """
        Updates the impact effect by changing its sprite every 2 frames and increments the time counter.

        The sprite is updated based on the current time divided by 2. If the time exceeds 10, the impact 
        effect is removed from the game by the Game class, which maintains a list of Impact instances.
        """
        
        # Impact sprites are numbered 0 to 4 (e.g. /images/impact0.png). We update to a new sprite 
        # every 2 frames by using integer division.
        self.image = "impact" + str(self.time // 2)

        # Increment the time counter
        self.time += 1
