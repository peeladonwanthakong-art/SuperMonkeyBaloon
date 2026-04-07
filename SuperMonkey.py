import pygame

pygame.init()

# Skapa fönster
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Svart ruta med ram")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Vit bakgrund

    # Rita svart fylld ruta
    pygame.draw.rect(screen, (0, 0, 0), (150, 150, 200, 200))

    # Rita ram (t.ex. röd)
    pygame.draw.rect(screen, (255, 0, 0), (150, 150, 200, 200), 5)

    pygame.display.flip()

pygame.quit()
