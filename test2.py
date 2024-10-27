import pygame
import sys
import math
import random
from os import listdir
from os.path import isfile, join

pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
GROUND_HEIGHT = 550

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Runner")

# Deal with sprites
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path =  join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)

# Define the player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, GROUND_HEIGHT - 60, 50, 50)
        self.color = BLUE
        self.gravity = 0.5
        self.velocity_y = 0
        self.jumping = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            
            # Prevent jumping infinitely
            if self.rect.y >= GROUND_HEIGHT - 60:
                self.rect.y = GROUND_HEIGHT - 60
                self.jumping = False
                self.velocity_y = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity_y = -10

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Define the Platform class
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Define the Obstacle class
class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Red color for obstacles

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Create player and platforms
player = Player()
platforms = [
    Platform(200, 450, 150, 20),
    Platform(400, 350, 150, 20),
    Platform(600, 250, 150, 20),
    Platform(800, 150, 150, 20)
]
obstacles = [
    Obstacle(300, GROUND_HEIGHT - 50, 50, 50),
    Obstacle(500, GROUND_HEIGHT - 50, 50, 50)
]

# Main game loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()

    # Move the player
    player.move(keys)

    # Apply gravity
    player.rect.y += player.velocity_y

    # Check for collisions with platforms
    on_ground = False
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            if player.velocity_y >= 0:  # Falling
                player.rect.bottom = platform.rect.top
                player.jumping = False
                player.velocity_y = 0
                on_ground = True  # The player is on a platform

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            if player.rect.bottom > obstacle.rect.top and player.rect.top < obstacle.rect.top:
                player.rect.bottom = obstacle.rect.top  # Land on top of the obstacle
                player.jumping = False
                player.velocity_y = 0
                on_ground = True  # The player is on an obstacle
            else:
                # Reset position if colliding from the sides
                if player.rect.right > obstacle.rect.left and player.rect.left < obstacle.rect.right:
                    if player.rect.centerx < obstacle.rect.centerx:
                        player.rect.right = obstacle.rect.left  # Push the player to the left
                    else:
                        player.rect.left = obstacle.rect.right  # Push the player to the right

    # If the player is not on the ground, apply gravity
    if not on_ground and player.rect.y < GROUND_HEIGHT - 60:
        player.velocity_y += player.gravity

    # Prevent falling through the ground
    if player.rect.y >= GROUND_HEIGHT - 60:
        player.rect.y = GROUND_HEIGHT - 60
        player.jumping = False
        player.velocity_y = 0

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the ground
    pygame.draw.rect(screen, ORANGE, (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))

    # Draw platforms and obstacles
    for platform in platforms:
        platform.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    # Draw the player
    player.draw(screen)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()