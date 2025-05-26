import pygame
import os

def create_player_sprite():
    # Create a surface for the player sprite
    width, height = 30, 50
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Colors
    body_color = (30, 144, 255)  # Dodger blue
    face_color = (255, 218, 185)  # Peach
    eye_color = (0, 0, 0)  # Black
    
    # Draw body (blue)
    pygame.draw.rect(image, body_color, (0, 10, width, height-10))
    
    # Draw head (peach circle)
    pygame.draw.circle(image, face_color, (width//2, 10), 10)
    
    # Draw eyes (black dots)
    pygame.draw.circle(image, eye_color, (width//2 - 3, 8), 2)
    pygame.draw.circle(image, eye_color, (width//2 + 3, 8), 2)
    
    # Draw arms
    pygame.draw.rect(image, body_color, (0, 15, 5, 20))  # Left arm
    pygame.draw.rect(image, body_color, (width-5, 15, 5, 20))  # Right arm
    
    # Draw legs
    pygame.draw.rect(image, (0, 0, 139), (5, height-15, 8, 15))  # Left leg
    pygame.draw.rect(image, (0, 0, 139), (width-13, height-15, 8, 15))  # Right leg
    
    # Save the image
    pygame.image.save(image, os.path.join('sprites', 'player.png'))
    
    return image

if __name__ == "__main__":
    pygame.init()
    create_player_sprite()
    pygame.quit()
