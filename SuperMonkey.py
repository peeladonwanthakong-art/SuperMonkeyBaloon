import pygame, sys

pygame.init()

skärm = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Meny")

vald_bakgrund = 1  # ← global state för bakgrund


def rita_bakgrund():
    if vald_bakgrund == 1:
        # Rutnät (mörkblå linjer)
        skärm.fill("black")
        for x in range(640 % 60, 1280, 60):
            pygame.draw.line(skärm, (25, 35, 55), (x, 0), (x, 720))
        for y in range(360 % 60, 720, 60):
            pygame.draw.line(skärm, (25, 35, 55), (0, y), (1280, y))


    elif vald_bakgrund == 2:
        # Röd/mörk arena-känsla som passar Block Fighter
        skärm.fill(("black"))
        for x in range(640 % 60, 1280, 60):
            pygame.draw.line(skärm, (80, 10, 10), (x, 0), (x, 720))
        for y in range(360 % 60, 720, 60):
            pygame.draw.line(skärm, (80, 10, 10), (0, y), (1280, y))
        pygame.draw.line(skärm, (120, 20, 20), (640, 0), (640, 720), 2)
        pygame.draw.line(skärm, (120, 20, 20), (0, 360), (1280, 360), 2)


def get_font(size):
    return pygame.font.Font(None, size)


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def refresss(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def kollar_input(self, position):
        return self.rect.collidepoint(position)

    def ändra_färg(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def play():
    klocka = pygame.time.Clock()
    px, py = 640.0, 360.0

    while True:
        klocka.tick(60)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        px += (mx - px) * 0.12
        py += (my - py) * 0.12

        rita_bakgrund()  # ← använder vald bakgrund

        pygame.draw.rect(skärm, "white", (px-25, py-25, 50, 50), border_radius=10)
        pygame.draw.rect(skärm, "black", (px-25, py-25, 50, 50), 2, border_radius=10)

        pygame.display.update()


def välj_bakgrund():
    global vald_bakgrund

    while True:
        rita_bakgrund()

        mus_posi = pygame.mouse.get_pos()
        bakgrund_text = get_font(80).render("Bakgrund", True, "#FF0B0B")
        bakgrund_rect = bakgrund_text.get_rect(center=(640, 80))
        skärm.blit(bakgrund_text, bakgrund_rect)

        bakgrund1_knapp = Button(image=None, pos=(640, 220),
                                 text_input="Blått rutnät", font=get_font(75),
                                 base_color="#6B0202", hovering_color="white")

        bakgrund2_knapp = Button(image=None, pos=(640, 340),
                                 text_input="Röd arena", font=get_font(75),
                                 base_color="#6B0202", hovering_color="white")

        bakgrund3_knapp = Button(image=None, pos=(640, 460),
                                 text_input="Bakgrund 3", font=get_font(75),
                                 base_color="#6B0202", hovering_color="white")
        
        tillbaka_knapp = Button(image=None, pos=(640, 670),
                                text_input="Tillbaka", font=get_font(50),
                                base_color="#FF0B0B", hovering_color="white")

        for button in [bakgrund1_knapp, bakgrund2_knapp, bakgrund3_knapp, tillbaka_knapp]:
            button.ändra_färg(mus_posi)
            button.refresss(skärm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tillbaka_knapp.kollar_input(mus_posi):
                    return
                if bakgrund1_knapp.kollar_input(mus_posi):
                    vald_bakgrund = 1
                if bakgrund2_knapp.kollar_input(mus_posi):
                    vald_bakgrund = 2
                if bakgrund3_knapp.kollar_input(mus_posi):
                    vald_bakgrund = 3

        pygame.display.update()


def inställningar():
    while True:
        rita_bakgrund()

        mus_posi = pygame.mouse.get_pos()
        settings_text = get_font(80).render("Inställningar", True, "#FF0B0B")
        settings_rect = settings_text.get_rect(center=(640, 80))
        skärm.blit(settings_text, settings_rect)

        musik_knapp = Button(image=None, pos=(640, 220),
                             text_input="Musik", font=get_font(75),
                             base_color="#6B0202", hovering_color="white")
        bakgrund_knapp = Button(image=None, pos=(640, 340),
                                text_input="Bakgrund", font=get_font(75),
                                base_color="#6B0202", hovering_color="white")
        skins_knapp = Button(image=None, pos=(640, 460),
                             text_input="Skins", font=get_font(75),
                             base_color="#6B0202", hovering_color="white")
        ljud_knapp = Button(image=None, pos=(640, 580),
                            text_input="Ljud", font=get_font(75),
                            base_color="#6B0202", hovering_color="white")
        tillbaka_knapp = Button(image=None, pos=(640, 670),
                                text_input="Tillbaka", font=get_font(50),
                                base_color="#FF0B0B", hovering_color="white")

        for button in [musik_knapp, bakgrund_knapp, skins_knapp, ljud_knapp, tillbaka_knapp]:
            button.ändra_färg(mus_posi)
            button.refresss(skärm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tillbaka_knapp.kollar_input(mus_posi):
                    return
                if bakgrund_knapp.kollar_input(mus_posi):
                    välj_bakgrund()

        pygame.display.update()


def main_menu():
    while True:
        rita_bakgrund()  # ← använder vald bakgrund i menyn också

        mus_posi = pygame.mouse.get_pos()

        meny_text = get_font(100).render("Block Fighter", True, "#FF0B0B")
        meny_rect = meny_text.get_rect(center=(640, 100))
        skärm.blit(meny_text, meny_rect)

        spela_knapp = Button(image=None, pos=(640, 250),
                             text_input="Spela", font=get_font(75),
                             base_color="#6B0202", hovering_color="White")
        settings_knapp = Button(image=None, pos=(640, 400),
                                text_input="Inställningar", font=get_font(75),
                                base_color="#6B0202", hovering_color="White")
        lämna_knapp = Button(image=None, pos=(640, 550),
                             text_input="Lämna", font=get_font(75),
                             base_color="#6B0202", hovering_color="White")

        for button in [spela_knapp, settings_knapp, lämna_knapp]:
            button.ändra_färg(mus_posi)
            button.refresss(skärm)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if spela_knapp.kollar_input(mus_posi):
                    play()
                if settings_knapp.kollar_input(mus_posi):
                    inställningar()
                if lämna_knapp.kollar_input(mus_posi):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()