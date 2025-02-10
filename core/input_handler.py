import pygame 
pygame.init()

WIDTH = 1000
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH,HEIGHT])


ghost_image = pygame.image.load("assets/sprites/sprite_ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (100, 100))

is_possessing = False


run = True
while run :
    screen.fill('white')
    timer.tick(fps)
    pygame.mouse.set_visible(False) #make the mouse cursor invisible
    mouse_position = pygame.mouse.get_pos() #obtain the position of the mouse in real time and store it in an array
    mouse_x = mouse_position[0] #can be deleted if not necessary for the calculations of the forces
    mouse_y = mouse_position[1] #can be deleted if not necessary for the calculations of the forces
    
    left_clicked = pygame.mouse.get_pressed()[0] #return a boolean : if left click is pressed or not (maintaining keep returning True)  
    
    
    
    
    if is_possessing is False:
        screen.blit(ghost_image, (mouse_x - ghost_image.get_width() // 2, mouse_y - ghost_image.get_height() // 2))  #display the ghost sprite such that the mouse is the center of the sprite
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            
        # Détecter quand l'utilisateur relâche le clic gauche
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_possessing = not is_possessing  # Inverser l'état seulement au relâchement
    
    pygame.display.flip()
pygame.quit()