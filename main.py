#main.py

import pygame
from editor.level_editor import LevelEditor

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Level Editor")
    clock = pygame.time.Clock()
    editor = LevelEditor(screen)

    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                editor.handle_event(event)
        
        editor.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()