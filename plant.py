from constants import *
from pygame import image, draw

class Plant:
    def __init__(self, x, y):
        self.energy = PLANT_ENERGY
        self.rect = None
        self.x = x
        self.y = y

    def draw(self, screen):
        # Load the Info image and the X image
        img = image.load(PLANT_IMG_PATH)

        # Draw the X image
        self.rect = img.get_rect()
        self.rect.topright = (self.x, self.y)
        screen.blit(img, self.rect)

    def remove(self, screen):
        """
        Remove this creature from the given surface.
        Removing by painting over it in the background's color.

        Args:
            surface (pygame.Surface): The surface on which to draw the creature.
        """
        draw.rect(screen, BACKGROUND_COLOR, self.rect)

