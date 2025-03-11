# Standard library imports
import math
import sys
import pgzero

# Local application constants
from src.constants import (MINIMUM_PYTHON_VERSION, 
                           MINIMUM_PYGAME_VERSION)


def check_python_pygame_versions():
    """
    Checks if the current Python and Pygame Zero versions meet the minimum required versions.
    
    This function performs the following checks:
    1. Verifies that the current Python version is at least the minimum required version.
    2. Verifies that the current Pygame Zero version is at least the minimum required version.
    
    If either of the version checks fail, the function prints an error message and exits the program.
    
    Raises:
        SystemExit: If the Python or Pygame Zero version is below the required minimum.
    """

    # Python version check
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        raise SystemExit(f"This game requires at least version {MINIMUM_PYTHON_VERSION} of Python. You have version {sys.version_info}. Please upgrade.")

    # Pygame version check
    pygame_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
    if pygame_version < MINIMUM_PYGAME_VERSION:
        raise SystemExit(f"This game requires at least version {MINIMUM_PYGAME_VERSION} of Pygame Zero. You have version {pgzero.__version__}. Please upgrade.")


def normalize_xy_vector(x, y):
    """
    Normalize a 2D vector (x, y) to a unit vector.

    This function takes the x and y components of a vector and returns a unit vector
    (a vector with a magnitude of 1) pointing in the same direction.

    Args:
        x (float): The x component of the vector.
        y (float): The y component of the vector.

    Returns:
        tuple: A tuple (x', y') representing the normalized unit vector.

    Raises:
        ValueError: If the length of the vector is zero, which would result in a division by zero.
    """

    # Calculate the length of the vector
    length = math.hypot(x, y)

    # Check if the length is zero
    if length == 0:
        raise ValueError("Cannot normalize a vector with zero length.")
    
    return (x / length, y / length)


def sign(x):
    """
    Determine the sign of a number.

    Parameters:
        x (int or float): The number to check.

    Returns:
        int: -1 if the number is negative, 1 if the number is positive or zero.
    """
    return -1 if x < 0 else 1
