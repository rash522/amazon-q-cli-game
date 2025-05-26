import pygame
import os

def create_platform_sprite():
    # Create a surface for the platform sprite
    width, height = 100, 20
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Colors
    platform_color = (139, 69, 19)  # Brown
    highlight_color = (160, 82, 45)  # Sienna
    
    # Draw main platform
    pygame.draw.rect(image, platform_color, (0, 0, width, height))
    
    # Draw top highlight
    pygame.draw.rect(image, highlight_color, (0, 0, width, 5))
    
    # Draw some texture lines
    for i in range(5, width-5, 20):
        pygame.draw.line(image, (101, 67, 33), (i, 8), (i+10, 8), 2)
        pygame.draw.line(image, (101, 67, 33), (i+5, 15), (i+15, 15), 2)
    
    # Save the image
    pygame.image.save(image, os.path.join('sprites', 'platform.png'))
    
    return image

if __name__ == "__main__":
    pygame.init()
    create_platform_sprite()
    pygame.quit()
