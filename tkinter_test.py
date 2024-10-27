import pygame
import os
import shutil
import subprocess

pygame.init()

# Constants and settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Target directory and preset file name
PRESET_NAME = "irlImage.jpg"
TARGET_DIR = os.path.join(os.getcwd(), "images/irl")

# Ensure the target directory exists
os.makedirs(TARGET_DIR, exist_ok=True)

def select_file_mac():
    try:
        result = subprocess.run(
            ['osascript', '-e', 'choose file of type {"public.image"}'],
            capture_output=True,
            text=True
        )
        file_path = result.stdout.strip().replace("alias ", "").replace(":", "/")
        if file_path:
            target_path = os.path.join(TARGET_DIR, PRESET_NAME)
            shutil.copy(file_path, target_path)
            print(f"Image saved to {target_path}")
            return target_path
    except Exception as e:
        print("Failed to select a file:", e)
    return None

# Pygame window setup
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Display")

# Load and set the selected image as background
bg_image_path = select_file_mac()
if bg_image_path:
    bg_img = pygame.image.load(bg_image_path)
else:
    bg_img = pygame.Surface((WIDTH, HEIGHT))  # Default blank surface if no image is chosen

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(bg_img, (0, 0))  # Draw background image
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
