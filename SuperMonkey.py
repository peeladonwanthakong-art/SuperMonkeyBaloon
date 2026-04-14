import pygame
import math
import random

pygame.init()

#skärm
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monkey Shooter")

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


# Färger
BLACK    = (20, 20, 20)
WHITE    = (255, 255, 255)
RED      = (220, 50, 50)
DARK_RED = (150, 20, 20)
PLAYER_COL = (30, 30, 30)
BG_COL   = (15, 25, 40)
BULLET_COL = (255, 220, 50)
UI_COL   = (100, 200, 255)
GREEN    = (50, 200, 80)

FONT      = pygame.font.SysFont("consolas", 22, bold=True)
BIG_FONT  = pygame.font.SysFont("consolas", 48, bold=True)
SMALL_FONT = pygame.font.SysFont("consolas", 16)

PLAYER_SIZE  = 30
ENEMY_SIZE   = 40
BULLET_SIZE  = 10
BULLET_SPEED = 300  
FIRE_RATE    = 0.5  

BULLET_SPEED = 150  

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = PLAYER_SIZE
        self.trail = []

    def update(self, mx, my):
        # Följer musen mjukt
        dx = mx - self.x
        dy = my - self.y
        self.x += dx * 0.12
        self.y += dy * 0.12

        # Håll inom skärm
        half = self.size // 2
        self.x = max(half, min(WIDTH - half, self.x))
        self.y = max(half, min(HEIGHT - half, self.y))
