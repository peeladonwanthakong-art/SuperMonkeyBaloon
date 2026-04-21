#Pee(förra lektionen)
import pygame, sys

pygame.init()

skärm = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Meny")


def get_font(size):
    return pygame.font.Font(None, size)

#Pee,Melvin,Andy(skit svårt att förstå kollade på en youtube video jätte bra)
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

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


#play()



#options()


#Färger Pee & Andy
def main_menu():
    while True:
        skärm.fill("black")

        mus_posi = pygame.mouse.get_pos()

        meny_text = get_font(100).render("Block Fighter", True, "#FF0B0B")
        meny_rect = meny_text.get_rect(center=(640, 100))
        skärm.blit(meny_text, meny_rect)
        
        #Färger Pee & Andy
        spela_knapp = Button(image=None, pos=(640, 250),
                             text_input="Spela", font=get_font(75),
                             base_color="#6B0202", hovering_color="White")
        settings_knapp= Button(image=None, pos=(640, 400),
                                text_input="Instälningar", font=get_font(75),
                                base_color="#6B0202", hovering_color="White")
        lämna_knapp = Button(image=None, pos=(640, 550),
                             text_input="Lämna", font=get_font(75),
                             base_color="#6B0202", hovering_color="White")

        for button in [spela_knapp, settings_knapp, lämna_knapp]:
            button.changeColor(mus_posi)
            button.update(skärm)
#Melvin
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if spela_knapp.checkForInput(mus_posi):
                    play()
                if settings_knapp.checkForInput(mus_posi):
                    options()
                if lämna_knapp.checkForInput(mus_posi):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
