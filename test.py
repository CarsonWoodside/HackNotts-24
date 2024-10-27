import pygame 

import tkinter as tk 

from tkinter import filedialog 

 

# Function to open file dialog 

def open_file_dialog(): 

    file_path = filedialog.askopenfilename(title="Select an Image",  

                                            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]) 

    return file_path 

 

# Initialize Pygame 

pygame.init() 

X = 600 

Y = 600 

scrn = pygame.display.set_mode((X, Y)) 

pygame.display.set_caption('Image Viewer') 

 

# Colors 

button_color = (0, 128, 255) 

button_hover_color = (0, 255, 255) 

text_color = (255, 255, 255) 

 

# Button dimensions 

button_rect = pygame.Rect(200, 250, 200, 50) 

 

# Main loop 

status = True 

loaded_image = None 

 

while status: 

    scrn.fill((0, 0, 0))  # Clear the screen 

 

    # Draw the button 

    if button_rect.collidepoint(pygame.mouse.get_pos()): 

        pygame.draw.rect(scrn, button_hover_color, button_rect) 

    else: 

        pygame.draw.rect(scrn, button_color, button_rect) 

 

    # Draw button text 

    font = pygame.font.Font(None, 36) 

    text = font.render('Open Image', True, text_color) 

    text_rect = text.get_rect(center=button_rect.center) 

    scrn.blit(text, text_rect) 

 

    # Display loaded image 

    if loaded_image: 

        scrn.blit(loaded_image, (0, 0)) 

 

    pygame.display.flip() 

 

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 

            status = False 

        if event.type == pygame.MOUSEBUTTONDOWN: 

            if event.button == 1 and button_rect.collidepoint(event.pos): 

                # Open file dialog and load image 

                root = tk.Tk() 

                root.withdraw()  # Hide the root window 

                file_path = open_file_dialog() 

                if file_path: 

                    try: 

                        loaded_image = pygame.image.load(file_path).convert() 

                    except pygame.error: 

                        print("Error loading image.") 

 

# Deactivate Pygame 

pygame.quit() 