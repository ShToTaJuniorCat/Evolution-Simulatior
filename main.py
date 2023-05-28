import pygame
from creature import Creature
from tools import *
from constants import *
import random
from plant import Plant


# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BACKGROUND_COLOR)
pygame.display.set_caption(WINDOW_NAME)
pygame.display.update()

# Load the Info image and the X image
x_img = pygame.image.load(X_IMG_PATH)

# Draw the X image
x_rect = x_img.get_rect()
x_rect.topright = screen.get_rect().topright
screen.blit(x_img, x_rect)

i_img = pygame.image.load(I_IMG_PATH)

# Draw the Info image
i_rect = i_img.get_rect()
i_rect.topright = (x_rect[0] - 15, 10)
screen.blit(i_img, i_rect)

# Create a list of creatures
creatures = [random_creature(CREATURE_RADIUS,
                             SCREEN_WIDTH - CREATURE_RADIUS,
                             CREATURE_RADIUS,
                             SCREEN_HEIGHT - CREATURE_RADIUS,
                             screen) for _ in range(NUM_CREATURES)]
creatures[0].special = True


plants = [Plant(randint(10, SCREEN_WIDTH - 10), randint(10, SCREEN_HEIGHT - 10)) for _ in range(PLANT_COUNT)]

flag = False
# Main game loop
running = True
while running:
    if len(creatures) == 0:
        print("restarted simulation")
        creatures = [random_creature(CREATURE_RADIUS, SCREEN_WIDTH - CREATURE_RADIUS, CREATURE_RADIUS, SCREEN_HEIGHT - CREATURE_RADIUS) for _ in range(NUM_CREATURES)]
    
    # Handle events
    for event in pygame.event.get():
        """
        Handles events such as quitting the game or clicking on the screen.
        """
        if event.type == pygame.QUIT:
            # Quit the game if the user clicks the i button in the top-right corner of the window
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if the user clicked the X button in the top-right corner of the window
            pos = pygame.mouse.get_pos()

            if x_rect.collidepoint(pos):
                running = False

            # Check if user clicked the Info button
            if i_rect.collidepoint(pos):
                print(simulation_info(creatures))

            # Check if the user clicked on any of the creatures
            if event.button == 1:
                # Only if the creatures are left clicked
                for creature in creatures:
                    # Calculate the distance between the mouse click and the center of the creature
                    # Then, check if the distance is less than the diameter of the creature
                    if creature.pygame_rect.collidepoint(pos): # ((creature.x - pos[0])**2 + (creature.y - pos[1]))**2 < CREATURE_RADIUS**2:
                        print(creature)
            elif event.button == 2:
                # Only if the creatures are middle clicked
                for creature in creatures:
                    # Calculate the distance between the mouse click and the center of the creature
                    # Then, check if the distance is less than the diameter of the creature
                    if creature.pygame_rect.collidepoint(pos):
                        creature.remove()
                        creatures.remove(creature)


    for plant in plants:
        plant.draw(screen)


    # Iterate over all creatures
    for creature in creatures:
        # The creature is now older.
        creature.time_alive += 1
        action = creature.take_action(plants)

        if action:
            creatures.append(action)
        
        # If the creature has less energy than allowed,
        # kill it.
        if creature.energy <= MIN_CREATURE_ENERGY:
            creature.remove()
            creatures.remove(creature)
            del creature

            
            continue

        # Draw all living creatures.
        creature.draw_body()
        creature.draw_eye()


        for plant in plants:
            if plant.rect.colliderect(creature.pygame_rect.inflate(CREATURE_PLANT_COLLISION_TOLERANCE, CREATURE_PLANT_COLLISION_TOLERANCE)):
                plant.remove(screen)
                creature.eat(plant)
                plants.remove(plant)
                del plant

                new_plant = Plant(randint(10, SCREEN_WIDTH - 10), randint(10, SCREEN_HEIGHT - 10))
                plants.append(new_plant)
                new_plant.draw(screen)


    screen.blit(x_img, x_rect)
    screen.blit(i_img, i_rect)

    # Update the display
    pygame.display.update()


# Quit Pygame
pygame.quit()
