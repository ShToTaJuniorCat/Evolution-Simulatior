from constants import *
from pygame import draw
from random import randint
from math import sin, cos, degrees, radians
from PIL import Image
from brain_inputs import *

class Creature:
    """
    Represents a creature in the evolution simulation.

    Attributes:
        x (int): The x-coordinate of the creature's location on the screen.
        y (int): The y-coordinate of the creature's location on the screen.
        color (tuple): The color of the creature in RGB format.
        name (str): The name of the creature.
    """


    @staticmethod
    def mutate(creature):
        if randint(1, int(1/COLOR_MUTATION_CHANCE)) == 1:
            for i in range(3):
                factor = randint(-5, 5)
                creature.color[i] = abs(creature.color[i] + factor) if creature.color[i] + factor <= 255 else 255

        if randint(1, int(1/X_MUTATION_CHANCE)) == 1:
            factor = randint(-5, 5)
            
            if creature.step + factor <= 10 and creature.step + factor >= -10:
                creature.step += factor

        creature.brain.mutate_weights()


    def __init__(self, x, y, color, name, radius, gen, brain, screen):
        """
        Initializes a new instance of the Creature class.

        Args:
            x (int): The initial x-coordinate of the creature's location on the screen.
            y (int): The initial y-coordinate of the creature's location on the screen.
            color (tuple): The initial color of the creature in RGB format.
            name (str): The name of the creature.
        """
        self.x = x
        self.y = y
        self.facing = 0
        self.step = 5
        self.color = list(color)
        self.name = name
        self.radius = radius
        self.time_alive = 0
        self.pygame_rect = None
        self.total_distance = 0
        self.gen = gen
        self.energy = START_ENERGY
        self.total_energy = START_ENERGY
        self.movement_energy_consumed = 0
        self.brain = brain
        self.brain.initialize_weights()
        self.screen = screen
        self.special = False
        self.reproduction_num = 0

    
    def __str__(self):
        return f"Creature '{self.name}' at position ({self.x},{self.y}) with color {self.color} and {self.energy} energy." \
               f"\nStep = {self.step}. Traveled {self.total_distance}. Currently facing {self.facing}°."


    def draw_body(self):
        """
        Draws this creature on the given surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the creature.
        """
        self.pygame_rect = draw.circle(self.screen, tuple(self.color), (self.x, self.y), self.radius)

    def draw_eye(self):
        draw.circle(self.screen, # surface
                    tuple(map(lambda x: abs(x - 255), self.color)), # color
                    (self.x + int(self.radius * cos(radians(self.facing))), self.y + int(self.radius * sin(radians(self.facing)))), # position
                    1) # radius

        
    def remove(self):
        """
        Remove this creature from the given surface.
        Removing by painting over it in the background's color.

        Args:
            surface (pygame.Surface): The surface on which to draw the creature.
        """
        draw.circle(self.screen, BACKGROUND_COLOR, (self.x, self.y), self.radius)
        draw.circle(self.screen, # surface
                    BACKGROUND_COLOR, # color
                    (self.x + int(self.radius * cos(radians(self.facing))), self.y + int(self.radius * sin(radians(self.facing)))), # position
                    1) # radius


    def get_inputs(self, plants):
        """
        The inputs are as follows, in order:
            - Index 0 corresponds to closest_plant_distance: the distance from the closest plant.
            - Index 1 corresponds to angle_from_closest_plant: the angle between the creature and the closest plant.
            - Index 2 corresponds to can_reproduce: a boolean value indicating if the creature can reproduce.
            - Index 3 corresponds to screen_edge_distance: the distance from the edge of the screen.
            - Index 4 corresponds to can_move_forward: a boolean value indicating if the creature can move forward.
            - Index 5 corresponds to energy_level: the current energy level of the creature.
                             
        The number of input values should match the number of input neurons in the neural network.
        """

        inputs = [closest_plant_distance(self, plants),
                  angle_from_closest_plant(self, plants),
                  int(can_reproduce(self)),
                  screen_edge_distance(self),
                  int(can_move_forward(self)),
                  self.energy]

        return inputs

    def take_action(self, plants):
        inputs = self.get_inputs(plants)
        self.brain.set_inputs(inputs)
        self.brain.mutate_weights()
        action, value = self.brain.decide_action()

        if self.special:
            print(f"Special creature: {inputs, action, value}")

##        if action == "reproduce":
##            offspring = self.reproduce()
##            return offspring
##        elif action == "move":
##            self.move(self.step * value)
##            return None
##        elif action == "turn":
##            self.turn(value * 360)
##            return None


    def eat(self, plant):
        self.energy += plant.energy
        self.total_energy += plant.energy


    def update_position(self, pixels):
        # calculate the new position of the creature
        new_x = self.x + int(pixels * cos(radians(self.facing)))
        new_y = self.y + int(pixels * sin(radians(self.facing)))

        # check if the new position is within the screen bounds
        if (new_x - self.radius >= 0) and (new_x + self.radius <= SCREEN_WIDTH) and (new_y - self.radius >= 0) and (new_y + self.radius <= SCREEN_HEIGHT):
            self.x = new_x
            self.y = new_y

        self.total_distance += pixels

    def move(self, pixels):
        self.energy -= MOVE_COST
        self.movement_energy_consumed += MOVE_COST
        self.remove()
        self.update_position(pixels)


    def duplicate(self):
        self.energy -= REPRODUCTION_COST

        return Creature(self.x, self.y, self.color, self.name, self.radius, self.gen + 1, self.brain, self.screen)


    def reproduce(self):
        offspring = self.duplicate()
        self.mutate(offspring)
        self.reproduction_num += 1

        return offspring


    def turn(self, angle):
        self.remove()
        
        self.facing += angle
        self.facing %= 360
        self.energy -= TURN_COST
        self.movement_energy_consumed += TURN_COST

        self.draw_body()
        self.draw_eye()
