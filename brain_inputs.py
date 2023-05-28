from math import sin, cos, degrees, radians, atan2, tan, acos
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, REPRODUCTION_COST


def sign(x):
    return int(abs(x)/x)


def points_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5


def closest_plant(creature, plants):
    return min(plants, key=lambda plant: points_distance((creature.x, creature.y), (plant.x, plant.y)))


def closest_plant_distance(creature, plants):
    plant = closest_plant(creature, plants)
    return points_distance((creature.x, creature.y), (plant.x, plant.y))


def angle_from_closest_plant(creature, plants):
    plant = closest_plant(creature, plants)

    difference_x = creature.x - plant.x
    difference_y = (-creature.y) - (-plant.y)
    angle = 180 - degrees(atan2(difference_y, difference_x))
    turn_angle = -(creature.facing - angle)
    return turn_angle % 360


def can_reproduce(creature):
    return creature.energy > REPRODUCTION_COST


def screen_edge_distance(creature):
    """
    Calculate distance to the the closest edge of the screen.
    The distance from the closest edge is the minimum distance from all the edges.
    """
    return min([creature.x, creature.y, SCREEN_WIDTH - creature.x, SCREEN_HEIGHT - creature.y])


def can_move_forward(creature):
    new_x = creature.x + int(creature.step * cos(radians(creature.facing)))
    new_y = creature.y + int(creature.step * sin(radians(creature.facing)))

    # check if the new position is within the screen bounds
    return (new_x - creature.radius >= 0) and (new_x + creature.radius <= SCREEN_WIDTH) and (new_y - creature.radius >= 0) and (new_y + creature.radius <= SCREEN_HEIGHT)
