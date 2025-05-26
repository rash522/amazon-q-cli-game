import pygame
import os

def create_coin_sprite():
    # Create a surface for the coin sprite
    size = 15
    image = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Colors
    coin_color = (255, 215, 0)  # Gold
    highlight_color = (255, 255, 200)  # Light yellow
    
    # Draw coin (circle)
    pygame.draw.circle(image, coin_color, (size//2, size//2), size//2)
    
    # Draw highlight (smaller circle inside)
    pygame.draw.circle(image, highlight_color, (size//3, size//3), size//6)
    
    # Draw a small "C" for coin
    font = pygame.font.SysFont(None, size)
    text = font.render("C", True, (200, 150, 0))
    text_rect = text.get_rect(center=(size//2, size//2))
    image.blit(text, text_rect)
    
    # Save the image
    pygame.image.save(image, os.path.join('sprites', 'coin.png'))
    
    return image

if __name__ == "__main__":
    pygame.init()
    create_coin_sprite()
    pygame.quit()
