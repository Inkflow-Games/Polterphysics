import pygame 
pygame.init()

WIDTH = 1000
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH,HEIGHT])

run = True
while run :
    screen.fill('white')
    timer.tick(fps)
    mouse_position = pygame.mouse.get_pos() #obtain the position of the mouse in real time and store it in an array
    print(mouse_position)
    pygame.draw.circle(screen, 'red', mouse_position, 16)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()
pygame.quit()