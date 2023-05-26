from string import ascii_letters, digits
from random import choice, randint
from pygame import draw
from creature import Creature
from constants import *
from brain import Brain


def generate_random_string(length):
    """
    Generates a random string of the given length, consisting of ASCII letters and digits.

    Args:
        length (int): The length of the random string to generate.

    Returns:
        str: A random string of the given length, consisting of ASCII letters and digits.
    """
    return ''.join(choice(ascii_letters + digits) for _ in range(length))


def random_creature(min_x, max_x, min_y, max_y, screen):
    """
    Generates a random creature within the given coordinate range.

    Args:
        min_x (int): The minimum x-coordinate of the creature's location on the screen.
        max_x (int): The maximum x-coordinate of the creature's location on the screen.
        min_y (int): The minimum y-coordinate of the creature's location on the screen.
        max_y (int): The maximum y-coordinate of the creature's location on the screen.

    Returns:
        Creature: A random instance of the Creature class with a random location, color, and name.
    """
    x = randint(min_x, max_x)
    y = randint(min_y, max_y)
    color = [randint(0, 255) for _ in range(3)]
    name = generate_random_string(16)

    return Creature(x, y, color, name, CREATURE_RADIUS, 1, Brain(NUM_INPUT_NEURONS, HIDDEN_LAYERS, NUM_OUTPUT_NEURONS), screen)


def simulation_info(creatures):
    avg_step = sum([creature.step for creature in creatures]) / len(creatures)
    last_gen = max([creature.gen for creature in creatures])
    
    return f"Creature start: {NUM_CREATURES}, current: {len(creatures)}\n"\
          f"The average step is {avg_step}. Latest generation is {last_gen}."


def points_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
