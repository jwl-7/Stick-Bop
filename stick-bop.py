import pygame
import random
import os

# look in dir that python file is in
os.chdir(os.path.dirname(__file__))

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700

# monokai color palette
white  = (253, 250, 243)
brown  = ( 45,  43,  46)
pink   = (255,  96, 137)
green  = (169, 220, 199)
yellow = (255, 216, 102)
orange = (252, 151, 105)
purple = (171, 157, 244)
blue   = (119, 220, 230)
black  = (  0,   0,   0)

score = 0

def main():
    pygame.init()
    size   = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    clock  = pygame.time.Clock()
    pygame.display.set_caption('Stick Bop! < TEST >')

    # display background image
    background_image = pygame.image.load('stick_pic.png').convert()
    screen.blit(background_image, [0, 0])

    # loop until user presses close button
    done = False

    # program loop
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # change image when key(left arrow) is pressed -- image stays after keypress
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.mixer.music.load('sword_ahhhh.wav')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(0)

                    image2 = pygame.image.load('stick_pic_sword.png').convert()
                    screen.blit(image2, [0, 0])

            # change image when key(left arrow) is released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    background_image = pygame.image.load('stick_pic.png').convert()
                    screen.blit(background_image, [0, 0])
                    
        # display score to screen into top right corner           
        game_font   = pygame.font.Font('OpenSans-Regular.ttf', 30)
        score_text  = 'Score: ' + str(score)
        score_label = game_font.render(score_text, 1, brown)
        screen.blit(score_label, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - (SCREEN_HEIGHT - 20)))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()