import pygame
pygame.init()

WIDTH = 1000
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

class Button:
    def __init__(self, size, x, y, height, width, text=''):
        self.size = size
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

    def press(self):
        mouse_position = pygame.mouse.get_pos()
        return pygame.mouse.get_pressed(num_buttons=3) == (True, False, False) and \
               (self.x - self.width / 2) < mouse_position[0] < (self.x + self.width / 2) and \
               (self.y - self.height / 2) < mouse_position[1] < (self.y + self.height / 2)

    def draw(self):
        pygame.draw.rect(screen, pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))

# Creating buttons
buttons = {
    "Play": Button(1, WIDTH / 2, HEIGHT / 2 - 20, 50, 100),
    "Pause": Button(1, WIDTH / 2, HEIGHT / 2 - 100, 50, 100),
    "Stop": Button(1, WIDTH / 2, HEIGHT / 2 + 80, 50, 100),
}

run = True
while run:
    # Clear the screen with a white background just once at the beginning of the loop
    screen.fill('white')
    
    # Draw all buttons in the correct order
    for button in buttons.values():
        button.draw()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Check for button presses and perform any necessary action
    for button in buttons.values():
        if button.press():
            print(f"{button.text} button pressed!")

    # Flip the display to update the screen after everything has been drawn
    pygame.display.flip()

    # Control the frame rate
    timer.tick(fps)

pygame.quit()