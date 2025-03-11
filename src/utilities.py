# Standard library imports
import math


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
