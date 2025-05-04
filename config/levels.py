import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

font = pygame.font.Font(None, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Détecte si la souris est sur le bouton
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, font, WHITE, screen, x + width // 2, y + height // 2)

def start_game():
    print("Lancement du jeu...")

def show_options():
    print("Ouverture des options...")

def quit_game():
    pygame.quit()
    quit()


def main_menu():
    running = True
    while running:
        screen.fill(GRAY)  # Fond du menu

        draw_text("Menu Principal", font, BLACK, screen, WIDTH // 2, 100)

        # Dessin des boutons
        draw_button("Jouer", 300, 200, 200, 50, RED, (255, 100, 100), start_game)
        draw_button("Options", 300, 300, 200, 50, RED, (255, 100, 100), show_options)
        draw_button("Quitter", 300, 400, 200, 50, RED, (255, 100, 100), quit_game)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()






 