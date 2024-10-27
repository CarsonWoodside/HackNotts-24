import pygame
from pygame.locals import *
from PIL import Image

img = Image.open("images/test2.jpeg")

target_size = (1000, 1000)
resized = img.resize(target_size)
resized.save("images/output.jpeg")

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

#images
bg_img = pygame.image.load('images/output.jpeg')

player = pygame.Rect((300, 200, 50, 50))


run = True
while run:

    screen.blit(bg_img, (0, 0))

    # key = pygame.key.get_pressed()
    # if key[pygame.K_a] == True:
    #     player.move_ip(-1, 0)
    # elif key[pygame.K_d] == True:
    #     player.move_ip(1, 0)
    # elif key[pygame.K_s] == True:
    #     player.move_ip(0, 1)
    # elif key[pygame.K_w] == True:
    #     player.move_ip(0, -1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()