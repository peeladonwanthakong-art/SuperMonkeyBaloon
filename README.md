# SuperMonkeyBaloon
import pygame
pygame.init()

bredd = 500
höjd = 500
screen = pygame.display.set_mode((bredd, höjd))
pygame.display.set_caption("Meny")

fps = 60
timer = pygame.time.Clock()  
main_meny= True
text = pygame.font.Font('freesansbold.ttf', 24)

run = True
while run:
    screen.fill((50, 0, 50))  
    timer.tick(fps)
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()  

def meny():
    spela_knapp = Button('Spela', (120, 180))
    lämna_knapp = Button('lämna', (120, 260))
    inst_knapp = Button('inställningar', (120, 320))
    spela_knapp.draw()
    inst_knapp.draw()
    lämna_knapp.draw()
    return not meny.check_clicked()
