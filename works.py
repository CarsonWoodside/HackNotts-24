import pygame
import sys
import math
import random
from os import listdir
from os.path import isfile, join

pygame.init()

# Constants and settings
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BG_GREY = (50, 50, 50)
CIRCLE_POSITION = (400, 300)
CIRCLE_RADIUS = 45
MAX_HEARTS = 3

# Game window setup
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image to Top Down Game")

# Load background images
bg_img = pygame.image.load('images/bw/threeBW.jpg')
bgOver_img = pygame.image.load('images/bw/three.jpg')

# Load heart image
heart_image = pygame.image.load('assets/hearts/heart.png')
heart_image = pygame.transform.scale(heart_image, (90, 90))

# Load candy images
candy_assets = ['assets/candy/candy1.png', 'assets/candy/candy2.png', 
                'assets/candy/candy3.png', 'assets/candy/candy4.png']

# Load player walking animations
walkRight = [pygame.image.load('assets/player/new/walk1.png'),
             pygame.image.load('assets/player/new/walk2.png'),
             pygame.image.load('assets/player/new/walk3.png'),
             pygame.image.load('assets/player/new/walk4.png'),
             pygame.image.load('assets/player/new/walk5.png')]

walkLeft = [pygame.image.load('assets/player/new/walk1.png'),
            pygame.image.load('assets/player/new/walk2.png'),
            pygame.image.load('assets/player/new/walk3.png'),
            pygame.image.load('assets/player/new/walk4.png'),
            pygame.image.load('assets/player/new/walk5.png')]

DEFAULT_IMAGE_SIZE = (50, 50)

# Load and scale idle character image
char = pygame.image.load('assets/player/new/idle.png')
char = pygame.transform.scale(char, DEFAULT_IMAGE_SIZE)

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
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
            all_sprites[image.replace(".png", "") + "_left"] = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites

# Constants for the player
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_INITIAL_POSITION = (100 - PLAYER_SIZE // 2, 300 - PLAYER_SIZE // 2)

# Game variables
score = 0
num_coins = 5
coins = []
game_running = True
game_won = False

class Player:
    SPRITES = load_sprite_sheets("player", "ghost", 32, 32, True)

    def __init__(self, initial_position, size, speed):
        self.pos = list(initial_position)
        self.angle = 0
        self.size = size
        self.speed = speed
        self.hearts = MAX_HEARTS
        self.is_damaged = False
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0

    def move(self, keys):
        if not self.isJump:
            if keys[pygame.K_w]:
                self.pos[0] += self.speed * math.sin(math.radians(self.angle))
                self.pos[1] -= self.speed * math.cos(math.radians(self.angle))
            if keys[pygame.K_s]:
                self.pos[0] -= self.speed * math.sin(math.radians(self.angle))
                self.pos[1] += self.speed * math.cos(math.radians(self.angle))
        else:
            if self.jumpCount >= -10:
                self.pos[1] -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.isJump = False

    def rotate(self, direction):
        self.angle += direction
        self.angle %= 360

    def draw(self, window):
        if self.walkCount >= len(walkLeft) * 3:
            self.walkCount = 0
        if keys[pygame.K_a]:
            walkLchar = pygame.transform.scale(walkLeft[self.walkCount // 3], DEFAULT_IMAGE_SIZE)
            rotated_surface = pygame.transform.rotate(walkLchar, -self.angle)
            self.walkCount += 1
        elif keys[pygame.K_d]:
            walkRchar = pygame.transform.scale(walkRight[self.walkCount // 3], DEFAULT_IMAGE_SIZE)
            rotated_surface = pygame.transform.rotate(walkRchar, -self.angle)
            self.walkCount += 1
        else:
            rotated_surface = pygame.transform.rotate(char, -self.angle)
            self.walkCount = 0

        rotated_rect = rotated_surface.get_rect(center=(self.pos[0] + self.size // 2, self.pos[1] + self.size // 2))
        window.blit(rotated_surface, rotated_rect.topleft)

    def reset(self, initial_position):
        self.pos = list(initial_position)
        self.angle = 0
        self.hearts = MAX_HEARTS
        self.is_damaged = False

def spawn_coins(num_coins):
    for _ in range(num_coins):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if bg_img.get_at((x, y))[:3] == WHITE[:3]:
                candy_asset = random.choice(candy_assets)
                candy_image = pygame.image.load(candy_asset)
                candy_image = pygame.transform.scale(candy_image, (30, 30))
                coins.append((candy_image, (x, y)))
                break

def reset_game():
    global score, coins, game_running, game_won
    player.reset(PLAYER_INITIAL_POSITION)
    score = 0
    coins.clear()
    spawn_coins(num_coins)
    game_running = True
    game_won = False

def draw_hearts():
    hearts_bg = pygame.Surface((MAX_HEARTS * 44, 40), pygame.SRCALPHA)
    hearts_bg.fill((*BG_GREY, 216))
    window.blit(hearts_bg, (20, 20))
    for i in range(player.hearts):
        window.blit(heart_image, (0 + i * 40, 0))

def draw_score():
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(topright=(WIDTH - 30, 30))
    score_bg = pygame.Surface(score_rect.inflate(20, 20).size, pygame.SRCALPHA)
    score_bg.fill((*BG_GREY, 216))
    window.blit(score_bg, score_rect.inflate(20, 20).topleft)
    window.blit(score_surface, score_rect)

def draw_win_screen():
    window.fill(BLACK)
    font = pygame.font.Font(None, 72)
    win_text = font.render("Congrats, you win!", True, WHITE)
    win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    window.blit(win_text, win_rect)

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    pygame.draw.rect(window, (50, 50, 200), button_rect.inflate(20, 10), border_radius=10)
    window.blit(button_text, button_rect)

    return button_rect

player = Player(PLAYER_INITIAL_POSITION, PLAYER_SIZE, PLAYER_SPEED)

# Spawn initial coins
spawn_coins(num_coins)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_won:
            if draw_win_screen().collidepoint(event.pos):
                reset_game()

    keys = pygame.key.get_pressed()

    if game_running:
        if keys[pygame.K_d]:
            player.rotate(-5)
        if keys[pygame.K_a]:
            player.rotate(5)

        player.move(keys)

        player_center_pos = (player.pos[0] + PLAYER_SIZE // 2, player.pos[1] + PLAYER_SIZE // 2)

        for candy_image, (x, y) in coins[:]:
            if math.hypot(candy_image.get_rect(center=(x, y)).center[0] - player_center_pos[0],
                           candy_image.get_rect(center=(x, y)).center[1] - player_center_pos[1]) < 30:
                score += 1
                coins.remove((candy_image, (x, y)))
                if score >= num_coins:
                    game_won = True
                    game_running = False

    # Draw everything
    window.blit(bg_img, (0, 0))
    if not game_running and not game_won:
        window.blit(bgOver_img, (0, 0))

    for candy_image, (x, y) in coins:
        window.blit(candy_image, (x, y))

    player.draw(window)
    draw_hearts()
    draw_score()

    if game_won:
        draw_win_screen()

    pygame.display.flip()
    clock.tick(FPS)
