import pygame 
import math

pygame.init() 

win = pygame.display.set_mode((800, 800)) 
pygame.display.set_caption("First Game") 

walkRight = [
    pygame.image.load('assets/player/new/walk1.png'), 
    pygame.image.load('assets/player/new/walk2.png'), 
    pygame.image.load('assets/player/new/walk3.png'), 
    pygame.image.load('assets/player/new/walk4.png'), 
    pygame.image.load('assets/player/new/walk5.png')
] 

walkLeft = [
    pygame.image.load('assets/player/new/walk1.png'), 
    pygame.image.load('assets/player/new/walk2.png'), 
    pygame.image.load('assets/player/new/walk3.png'), 
    pygame.image.load('assets/player/new/walk4.png'), 
    pygame.image.load('assets/player/new/walk5.png')
] 

bg = pygame.image.load('images/bw/threeBW.jpg') 
char = pygame.image.load('assets/player/new/idle.png') 
DEFAULT_IMAGE_SIZE = (50, 50)
char = pygame.transform.scale(char, DEFAULT_IMAGE_SIZE)

x, y = 400, 400  # Start in the center of the window
angle = 0  # Initialize angle for rotation
vel = 5 
clock = pygame.time.Clock() 

isJump = False 
jumpCount = 10 
walkCount = 0 

def redrawGameWindow(): 
    global walkCount 
    win.blit(bg, (0, 0))   
    if walkCount >= len(walkLeft) * 3: 
        walkCount = 0 
    if left:   
        walkLchar = pygame.transform.scale(walkLeft[walkCount // 3], DEFAULT_IMAGE_SIZE)
        rotated_char = pygame.transform.rotate(walkLchar, angle)
        win.blit(rotated_char, (x - rotated_char.get_width() // 2, y - rotated_char.get_height() // 2)) 
        walkCount += 1                           
    elif right: 
        walkRchar = pygame.transform.scale(walkRight[walkCount // 3], DEFAULT_IMAGE_SIZE)
        rotated_char = pygame.transform.rotate(walkRchar, angle)
        win.blit(rotated_char, (x - rotated_char.get_width() // 2, y - rotated_char.get_height() // 2)) 
        walkCount += 1 
    else: 
        rotated_char = pygame.transform.rotate(char, angle)
        win.blit(rotated_char, (x - rotated_char.get_width() // 2, y - rotated_char.get_height() // 2)) 
        walkCount = 0 
    pygame.display.update() 

run = True 

while run: 
    clock.tick(27) 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False 

    keys = pygame.key.get_pressed() 
    left = keys[pygame.K_a] 
    right = keys[pygame.K_d] 

    if left: 
        angle += 5  # Rotate left
    if right: 
        angle -= 5  # Rotate right

    if not isJump: 
        if keys[pygame.K_w]:  # Move up
            y -= vel * math.cos(math.radians(angle))  # Move in the direction of the angle
            x -= vel * math.sin(math.radians(angle))
        if keys[pygame.K_s]:  # Move down
            y += vel * math.cos(math.radians(angle))  # Move in the opposite direction
            x -= vel * math.sin(math.radians(angle))
        if keys[pygame.K_SPACE]: 
            isJump = True 
            walkCount = 0 
    else: 
        if jumpCount >= -10: 
            y -= (jumpCount * abs(jumpCount)) * 0.5 
            jumpCount -= 1 
        else:  
            jumpCount = 10 
            isJump = False 

    redrawGameWindow() 

pygame.quit()
