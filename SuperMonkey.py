import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monkey Shooter 🐒")

clock = pygame.time.Clock()

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
BULLET_SPEED = 300  # pixlar per sekund (0.5 rutor/sek skalas upp för spelbarhet; se not)
FIRE_RATE    = 0.5  # sekunder mellan skott

# Not: "0.5 rutor per sekund" tolkas som att en kula tar 2 sekunder att traversera
# ett fält. Vi använder 300 px/s för bra spelupplevelse men skalar det snyggt.
BULLET_SPEED = 150  # pixlar/sek  ≈ 0.5 "rutor" per sek om ruta = 300px


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

        # Spara trail
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 15:
            self.trail.pop(0)

    def draw(self, surf):
        # Rita trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.3)
            r = max(4, int(self.size * 0.4 * (i / len(self.trail))))
            pygame.draw.rect(surf, (60, 60, 80),
                             (tx - r // 2, ty - r // 2, r, r), border_radius=2)

        # Rita spelaren (svart ruta med kant)
        rect = pygame.Rect(self.x - self.size // 2,
                           self.y - self.size // 2,
                           self.size, self.size)
        pygame.draw.rect(surf, PLAYER_COL, rect, border_radius=4)
        pygame.draw.rect(surf, UI_COL, rect, 2, border_radius=4)

        # Liten markör/öga
        pygame.draw.circle(surf, UI_COL, (int(self.x), int(self.y)), 4)

    def get_rect(self):
        half = self.size // 2
        return pygame.Rect(self.x - half, self.y - half, self.size, self.size)


class Enemy:
    def __init__(self):
        self.size = ENEMY_SIZE
        self.hp = 3
        self.max_hp = 3
        self.spawn()
        self.shake_timer = 0

    def spawn(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.x = random.randint(50, WIDTH - 50)
            self.y = -self.size
        elif side == "bottom":
            self.x = random.randint(50, WIDTH - 50)
            self.y = HEIGHT + self.size
        elif side == "left":
            self.x = -self.size
            self.y = random.randint(50, HEIGHT - 50)
        else:
            self.x = WIDTH + self.size
            self.y = random.randint(50, HEIGHT - 50)

        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

    def update(self, px, py, dt):
        # Rör sig sakta mot spelaren
        dx = px - self.x
        dy = py - self.y
        dist = max(1, math.hypot(dx, dy))
        speed = 60
        self.x += (dx / dist) * speed * dt + self.vx
        self.y += (dy / dist) * speed * dt + self.vy

        if self.shake_timer > 0:
            self.shake_timer -= dt

    def hit(self):
        self.hp -= 1
        self.shake_timer = 0.15

    def draw(self, surf):
        sx = int(self.x + (random.randint(-3, 3) if self.shake_timer > 0 else 0))
        sy = int(self.y + (random.randint(-3, 3) if self.shake_timer > 0 else 0))
        half = self.size // 2

        # Kropp
        rect = pygame.Rect(sx - half, sy - half, self.size, self.size)
        pygame.draw.rect(surf, RED, rect, border_radius=5)
        pygame.draw.rect(surf, DARK_RED, rect, 2, border_radius=5)

        # HP-bar
        bar_w = self.size
        bar_h = 5
        bar_x = sx - half
        bar_y = sy - half - 10
        pygame.draw.rect(surf, DARK_RED, (bar_x, bar_y, bar_w, bar_h))
        hp_w = int(bar_w * (self.hp / self.max_hp))
        pygame.draw.rect(surf, GREEN, (bar_x, bar_y, hp_w, bar_h))

    def get_rect(self):
        half = self.size // 2
        return pygame.Rect(self.x - half, self.y - half, self.size, self.size)


class Bullet:
    def __init__(self, x, y, tx, ty):
        self.x = x
        self.y = y
        self.size = BULLET_SIZE
        dx = tx - x
        dy = ty - y
        dist = max(1, math.hypot(dx, dy))
        self.vx = (dx / dist) * BULLET_SPEED
        self.vy = (dy / dist) * BULLET_SPEED
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if (self.x < -20 or self.x > WIDTH + 20 or
                self.y < -20 or self.y > HEIGHT + 20):
            self.alive = False

    def draw(self, surf):
        half = self.size // 2
        rect = pygame.Rect(int(self.x) - half, int(self.y) - half,
                           self.size, self.size)
        pygame.draw.rect(surf, BULLET_COL, rect, border_radius=2)
        # Liten glöd
        glow = pygame.Rect(int(self.x) - half - 2, int(self.y) - half - 2,
                           self.size + 4, self.size + 4)
        pygame.draw.rect(surf, (255, 180, 0, 80), glow, 1, border_radius=3)

    def get_rect(self):
        half = self.size // 2
        return pygame.Rect(int(self.x) - half, int(self.y) - half,
                           self.size, self.size)


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 180)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.3, 0.7)
        self.max_life = self.life
        self.size = random.randint(3, 8)
        self.color = color

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.9
        self.vy *= 0.9
        self.life -= dt

    def draw(self, surf):
        alpha = self.life / self.max_life
        r, g, b = self.color
        col = (int(r * alpha), int(g * alpha), int(b * alpha))
        s = max(1, int(self.size * alpha))
        pygame.draw.rect(surf, col,
                         (int(self.x) - s // 2, int(self.y) - s // 2, s, s))


def spawn_enemies(count=5):
    return [Enemy() for _ in range(count)]


def draw_grid(surf):
    for x in range(0, WIDTH, 60):
        pygame.draw.line(surf, (25, 35, 55), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 60):
        pygame.draw.line(surf, (25, 35, 55), (0, y), (WIDTH, y))


def draw_ui(surf, score, wave, fire_timer):
    # Score
    s = FONT.render(f"POÄNG: {score}", True, UI_COL)
    surf.blit(s, (15, 15))
    # Wave
    w = FONT.render(f"VÅG: {wave}", True, WHITE)
    surf.blit(w, (15, 42))
    # Fire cooldown bar
    bar_w = 100
    cd_frac = max(0, 1 - fire_timer / FIRE_RATE)
    pygame.draw.rect(surf, (40, 40, 60), (WIDTH - 120, 15, bar_w, 12), border_radius=4)
    pygame.draw.rect(surf, BULLET_COL, (WIDTH - 120, 15, int(bar_w * cd_frac), 12), border_radius=4)
    lbl = SMALL_FONT.render("SKJUT", True, (180, 180, 180))
    surf.blit(lbl, (WIDTH - 120, 30))


def game_over_screen(surf, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surf.blit(overlay, (0, 0))
    go = BIG_FONT.render("GAME OVER", True, RED)
    surf.blit(go, (WIDTH // 2 - go.get_width() // 2, HEIGHT // 2 - 80))
    sc = FONT.render(f"Slutpoäng: {score}", True, WHITE)
    surf.blit(sc, (WIDTH // 2 - sc.get_width() // 2, HEIGHT // 2))
    restart = FONT.render("Tryck SPACE för att spela igen", True, UI_COL)
    surf.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 50))


def main():
    player = Player()
    enemies = spawn_enemies(5)
    bullets = []
    particles = []

    score = 0
    wave = 1
    fire_timer = 0
    game_over = False
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key == pygame.K_SPACE:
                    # Starta om
                    player = Player()
                    enemies = spawn_enemies(5)
                    bullets = []
                    particles = []
                    score = 0
                    wave = 1
                    fire_timer = 0
                    game_over = False

        if not game_over:
            # Uppdatera spelaren
            player.update(mx, my)

            # Skjutning (automatisk mot närmaste fiende)
            fire_timer = max(0, fire_timer - dt)
            if fire_timer == 0 and enemies:
                # Hitta närmaste fiende
                nearest = min(enemies,
                              key=lambda e: math.hypot(e.x - player.x, e.y - player.y))
                bullets.append(Bullet(player.x, player.y, nearest.x, nearest.y))
                fire_timer = FIRE_RATE

            # Uppdatera kulor
            for b in bullets:
                b.update(dt)
            bullets = [b for b in bullets if b.alive]

            # Uppdatera fiender
            for e in enemies:
                e.update(player.x, player.y, dt)

            # Kollision kula <-> fiende
            for b in bullets[:]:
                for e in enemies[:]:
                    if b.get_rect().colliderect(e.get_rect()):
                        b.alive = False
                        e.hit()
                        # Partiklar
                        for _ in range(8):
                            particles.append(Particle(e.x, e.y, (220, 80, 80)))
                        if e.hp <= 0:
                            score += 10
                            enemies.remove(e)
                            for _ in range(15):
                                particles.append(Particle(e.x, e.y, (255, 120, 50)))
                        break

            # Kollision spelare <-> fiende → game over
            for e in enemies:
                if player.get_rect().colliderect(e.get_rect()):
                    game_over = True

            # Ny våg om alla fiender döda
            if not enemies:
                wave += 1
                count = 5 + (wave - 1) * 2
                enemies = spawn_enemies(count)

            # Uppdatera partiklar
            for p in particles:
                p.update(dt)
            particles = [p for p in particles if p.life > 0]

        # Rita
        screen.fill(BG_COL)
        draw_grid(screen)

        for p in particles:
            p.draw(screen)

        for e in enemies:
            e.draw(screen)

        for b in bullets:
            b.draw(screen)

        player.draw(screen)

        draw_ui(screen, score, wave, fire_timer)

        if game_over:
            game_over_screen(screen, score)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()