import pygame
import os

def create_enemy_sprite():
    # Create a surface for the enemy sprite
    size = 30
    image = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colors
    body_color = (255, 0, 0)  # Red
    eye_color = (255, 255, 255)  # White
    pupil_color = (0, 0, 0)  # Black
    
    # Draw body (red circle)
    pygame.draw.circle(image, body_color, (size//2, size//2), size//2)
    
    # Draw eyes (white circles)
    eye_size = size // 6
    pygame.draw.circle(image, eye_color, (size//3, size//3), eye_size)
    pygame.draw.circle(image, eye_color, (2*size//3, size//3), eye_size)
    
    # Draw pupils (black dots)
    pygame.draw.circle(image, pupil_color, (size//3, size//3), eye_size//2)
    pygame.draw.circle(image, pupil_color, (2*size//3, size//3), eye_size//2)
    
    # Draw angry eyebrows
    pygame.draw.line(image, pupil_color, (size//4, size//4), (size//2 - 2, size//3 - 2), 2)
    pygame.draw.line(image, pupil_color, (3*size//4, size//4), (size//2 + 2, size//3 - 2), 2)
    
    # Draw mouth (angry)
    pygame.draw.arc(image, pupil_color, (size//4, size//2, size//2, size//3), 3.14, 2*3.14, 2)
    
    # Save the image
    pygame.image.save(image, os.path.join('sprites', 'enemy.png'))
    
    return image

if __name__ == "__main__":
    pygame.init()
    create_enemy_sprite()
    pygame.quit()
