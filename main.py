import pygame
from pygame.math import Vector2
from core.physics_engine import PhysicsEngine
from objects.object import Object

# Initialize Pygame
pygame.init()

# Configure the window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Physics Engine Test")

# Physics engine initialization
physics_engine = PhysicsEngine()

# Create an object for testing
test_object = Object(mass=2, position=(400, 100), damping_coefficient=Vector2(0.93, 0.94), max_speed=100)
physics_engine.add_object(test_object)

# Clock to manage the frame rate
clock = pygame.time.Clock()
running = True

# Dictionary to manage the state of keys (whether a key is pressed or not)
key_state = {
    pygame.K_RIGHT: False,
    pygame.K_LEFT: False,
    pygame.K_DOWN: False,
    pygame.K_UP: False
}

# Main game loop
while running:
    # Handle events (such as quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop if the close button is clicked

    # Get the current state of all keys
    keys = pygame.key.get_pressed()

    # Apply force to the object if the corresponding key is pressed and hasn't been pressed already
    # Right force (to the right)
    if keys[pygame.K_RIGHT] and not key_state[pygame.K_RIGHT]:
        test_object.apply_force(Vector2(50, 0))  # Apply force to the right
        key_state[pygame.K_RIGHT] = True  # Mark that the key has been pressed

    # Left force (to the left)
    if keys[pygame.K_LEFT] and not key_state[pygame.K_LEFT]:
        test_object.apply_force(Vector2(-50, 0))  # Apply force to the left
        key_state[pygame.K_LEFT] = True  # Mark that the key has been pressed

    # Downward force (towards the bottom)
    if keys[pygame.K_DOWN] and not key_state[pygame.K_DOWN]:
        test_object.apply_force(Vector2(0, 50))  # Apply force downward
        key_state[pygame.K_DOWN] = True  # Mark that the key has been pressed

    # Upward force (towards the top)
    if keys[pygame.K_UP] and not key_state[pygame.K_UP]:
        test_object.apply_force(Vector2(0, -50))  # Apply force upward
        key_state[pygame.K_UP] = True  # Mark that the key has been pressed

    # Check if a key has been released and reset its state to allow the next press
    for key in key_state:
        if not keys[key]:
            key_state[key] = False

    # Update the physics engine, using the delta time (time passed since the last frame)
    dt = clock.get_time() / 100.0  # Time elapsed in seconds
    physics_engine.update(dt)

    # Draw the object
    screen.fill((0, 0, 0))  # Clear the screen with black color
    pygame.draw.circle(screen, (255, 0, 0), (int(test_object.position.x), int(test_object.position.y)), 10)
    
    # Display the position of the object for debugging purposes
    font = pygame.font.SysFont("Arial", 24)
    position_text = font.render(f"Position: ({int(test_object.position.x)}, {-int(test_object.position.y)})", True, (255, 255, 255))
    screen.blit(position_text, (10, 10))  # Blit the position text on the screen

    # Refresh the screen to display the updates
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame once the game loop ends
pygame.quit()
