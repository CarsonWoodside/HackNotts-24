import pygame
import sys

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))

rectangle_color = (0, 0, 255)
rectangle_position = [width // 2, height // 2]
rectangle_size = [50, 50]
rectangle_speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        rectangle_position[1] -= rectangle_speed
    if keys[pygame.K_s]:
        rectangle_position[1] += rectangle_speed
    if keys[pygame.K_a]:
        rectangle_position[0] -= rectangle_speed
    if keys[pygame.K_d]:
        rectangle_position[0] += rectangle_speed

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, rectangle_color, (rectangle_position[0], rectangle_position[1], rectangle_size[0], rectangle_size[1]))
    pygame.display.flip()
    pygame.time.Clock().tick(60)
