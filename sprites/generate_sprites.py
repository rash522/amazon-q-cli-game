import pygame
import os
from player import create_player_sprite
from platform import create_platform_sprite
from coin import create_coin_sprite
from enemy import create_enemy_sprite

def main():
    pygame.init()
    
    # Create sprites directory if it doesn't exist
    if not os.path.exists('sprites'):
        os.makedirs('sprites')
    
    # Generate all sprites
    create_player_sprite()
    create_platform_sprite()
    create_coin_sprite()
    create_enemy_sprite()
    
    print("All sprites generated successfully!")
    pygame.quit()

if __name__ == "__main__":
    main()
