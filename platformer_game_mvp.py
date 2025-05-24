import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer MVP")
clock = pygame.time.Clock()

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(GOLD)
        pygame.draw.circle(self.image, GOLD, (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Animation variables
        self.animation_timer = 0
        self.original_y = y
        
    def update(self):
        # Make coin bob up and down slightly
        self.animation_timer += 0.1
        self.rect.y = self.original_y + int(3 * math.sin(self.animation_timer))

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.velocity = 2
        self.facing_right = True
    
    def update(self):
        self.rect.x += self.velocity
        
        if self.rect.left <= self.min_x or self.rect.right >= self.max_x:
            self.velocity *= -1

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        
        # Movement variables
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
    
    def update(self, platforms):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Move horizontally
        self.rect.x += self.velocity_x
        
        # Check for horizontal collisions
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.velocity_x > 0:  # Moving right
                self.rect.right = platform.rect.left
            elif self.velocity_x < 0:  # Moving left
                self.rect.left = platform.rect.right
        
        # Move vertically
        self.rect.y += self.velocity_y
        
        # Check for vertical collisions
        self.on_ground = False
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.velocity_y > 0:  # Falling
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif self.velocity_y < 0:  # Jumping
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
        
        # Keep player on screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
    
    def move_left(self):
        self.velocity_x = -PLAYER_SPEED
    
    def move_right(self):
        self.velocity_x = PLAYER_SPEED
    
    def stop(self):
        self.velocity_x = 0

# Create platforms, coins and enemies for the level
def create_level():
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    # Ground platform
    ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
    platforms.add(ground)
    
    # Add some platforms
    platform_data = [
        (100, 400, 200, 20),
        (400, 300, 150, 20),
        (250, 200, 100, 20),
        (550, 450, 200, 20),
        (650, 200, 150, 20)
    ]
    
    for x, y, width, height in platform_data:
        platforms.add(Platform(x, y, width, height))
        
        # Add coins on some platforms
        if random.random() > 0.3:  # 70% chance to spawn a coin
            coins.add(Coin(x + width // 2, y - 25))
        
        # Add enemies on some platforms
        if width > 100 and random.random() > 0.5:  # 50% chance to spawn an enemy on wide platforms
            enemies.add(Enemy(x + width // 2, y - 30, x, x + width))
    
    return platforms, coins, enemies

# Draw text on screen
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Main game loop
def main():
    # Game variables
    score = 0
    lives = 3
    game_state = MENU
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    
    # Create platforms, coins, and enemies
    platforms, coins, enemies = create_level()
    all_sprites.add(platforms)
    all_sprites.add(coins)
    all_sprites.add(enemies)
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == PLAYING:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        player.jump()
                elif game_state == MENU:
                    if event.key == pygame.K_RETURN:
                        game_state = PLAYING
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        # Reset game
                        score = 0
                        lives = 3
                        all_sprites = pygame.sprite.Group()
                        platforms, coins, enemies = create_level()
                        all_sprites.add(platforms)
                        all_sprites.add(coins)
                        all_sprites.add(enemies)
                        player = Player()
                        all_sprites.add(player)
                        game_state = PLAYING
        
        if game_state == PLAYING:
            # Get keyboard state for continuous movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            elif keys[pygame.K_RIGHT]:
                player.move_right()
            else:
                player.stop()
            
            # Update game state
            player.update(platforms)
            enemies.update()
            coins.update()
            
            # Check for coin collisions
            coin_hits = pygame.sprite.spritecollide(player, coins, True)
            for coin in coin_hits:
                score += 10
            
            # Check for enemy collisions
            enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
            if enemy_hits:
                lives -= 1
                player.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                player.velocity_y = 0
                
                if lives <= 0:
                    game_state = GAME_OVER
            
            # Check if player fell off the screen
            if player.rect.top > SCREEN_HEIGHT:
                lives -= 1
                player.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                player.velocity_y = 0
                
                if lives <= 0:
                    game_state = GAME_OVER
        
        # Draw everything
        screen.fill(SKY_BLUE)
        
        # Draw simple clouds
        for _ in range(5):
            cloud_x = (pygame.time.get_ticks() // 50 + _ * 200) % (SCREEN_WIDTH + 200) - 100
            cloud_y = 50 + _ * 30
            pygame.draw.ellipse(screen, WHITE, (cloud_x, cloud_y, 70, 30))
        
        # Draw sprites
        all_sprites.draw(screen)
        
        # Draw score and lives
        draw_text(f"Score: {score}", 36, WHITE, 100, 10)
        draw_text(f"Lives: {lives}", 36, WHITE, 700, 10)
        
        # Draw game state screens
        if game_state == MENU:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            draw_text("2D PLATFORMER", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            draw_text("Collect coins and avoid enemies", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text("Press ENTER to start", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
        
        elif game_state == GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            draw_text("GAME OVER", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            draw_text(f"Final Score: {score}", 48, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text("Press ENTER to play again", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
