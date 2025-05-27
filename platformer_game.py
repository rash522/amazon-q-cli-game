import pygame
import sys
import random
import math
import os

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
TRANSPARENT = (0, 0, 0, 0)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
CONTROLS = 3

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced 2D Platformer")
clock = pygame.time.Clock()

# Load sprites
def load_sprite(filename, scale=1):
    try:
        sprite_path = os.path.join('sprites', 'sprites', filename)
        image = pygame.image.load(sprite_path).convert_alpha()
        if scale != 1:
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image
    except pygame.error as e:
        print(f"Unable to load sprite image {filename}: {e}")
        # Create a placeholder surface
        surface = pygame.Surface((30, 30))
        surface.fill(RED)
        return surface

# Load sprites
player_sprite = load_sprite('player.png')
platform_sprite = load_sprite('platform.png')
coin_sprite = load_sprite('coin.png')
enemy_sprite = load_sprite('enemy.png')

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Scale the platform sprite to the desired width and height
        self.image = pygame.transform.scale(platform_sprite, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_sprite
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
        self.image = enemy_sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.velocity = 2
        self.facing_right = True
        self.original_image = self.image
    
    def update(self):
        self.rect.x += self.velocity
        
        # Flip the sprite based on direction
        if self.velocity > 0 and not self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.facing_right = True
        elif self.velocity < 0 and self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.facing_right = False
        
        if self.rect.left <= self.min_x or self.rect.right >= self.max_x:
            self.velocity *= -1

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_sprite
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        
        # Movement variables
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.original_image = self.image
    
    def update(self, platforms):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Move horizontally
        self.rect.x += self.velocity_x
        
        # Update sprite direction
        if self.velocity_x > 0 and not self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.facing_right = True
        elif self.velocity_x < 0 and self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.facing_right = False
        
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

# Button class for menu
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.action:
                return self.action()
        return None

# Create platforms, coins and enemies for the level
def create_level(level=1):
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    # Ground platform
    ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
    platforms.add(ground)
    
    # Add platforms based on level
    if level == 1:
        platform_data = [
            (100, 400, 200, 20),
            (400, 300, 150, 20),
            (250, 200, 100, 20),
            (550, 450, 200, 20),
            (650, 200, 150, 20)
        ]
    elif level == 2:
        platform_data = [
            (50, 450, 150, 20),
            (300, 400, 100, 20),
            (500, 350, 100, 20),
            (650, 250, 150, 20),
            (400, 200, 100, 20),
            (200, 150, 100, 20),
            (50, 250, 100, 20)
        ]
    else:  # Level 3 and beyond
        platform_data = []
        for i in range(8):
            x = random.randint(50, SCREEN_WIDTH - 150)
            y = 150 + i * 60
            width = random.randint(80, 200)
            platform_data.append((x, y, width, 20))
    
    for x, y, width, height in platform_data:
        platforms.add(Platform(x, y, width, height))
        
        # Add coins on platforms
        if random.random() > 0.3:  # 70% chance to spawn a coin
            coins.add(Coin(x + width // 2, y - 25))
        
        # Add enemies on some platforms (more enemies in higher levels)
        if width > 100 and random.random() > (0.6 - level * 0.1):
            enemies.add(Enemy(x + width // 2, y - 30, x, x + width))
    
    # Ensure there's at least 3 coins per level
    if len(coins) < 3:
        for _ in range(3 - len(coins)):
            platform = random.choice(list(platforms)[1:])  # Skip ground platform
            coins.add(Coin(platform.rect.centerx, platform.rect.top - 25))
    
    return platforms, coins, enemies

# Draw text on screen
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Draw background with parallax effect
def draw_background(level):
    # Sky
    if level == 1:
        sky_color = SKY_BLUE
    elif level == 2:
        sky_color = (100, 150, 200)  # Evening sky
    else:
        sky_color = (20, 20, 50)  # Night sky
    
    screen.fill(sky_color)
    
    # Draw clouds or stars based on level
    if level <= 2:
        # Draw clouds
        for i in range(5):
            cloud_x = (pygame.time.get_ticks() // 50 + i * 200) % (SCREEN_WIDTH + 200) - 100
            cloud_y = 50 + i * 30
            pygame.draw.ellipse(screen, WHITE, (cloud_x, cloud_y, 70, 30))
    else:
        # Draw stars
        for i in range(20):
            star_x = (i * 40 + pygame.time.get_ticks() // 100) % SCREEN_WIDTH
            star_y = i * 25 % (SCREEN_HEIGHT - 100)
            pygame.draw.circle(screen, WHITE, (star_x, star_y), 2)

# Main game loop
def main():
    # Game variables
    score = 0
    lives = 3
    level = 1
    game_state = MENU
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    # Create platforms, coins, and enemies
    platforms, coins, enemies = create_level(level)
    all_sprites.add(platforms)
    all_sprites.add(coins)
    all_sprites.add(enemies)
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Create menu buttons
    start_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50, "Start Game", GREEN, (100, 255, 100), 
                         lambda: "start")
    controls_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50, "Controls", YELLOW, (255, 255, 100), 
                            lambda: "controls")
    quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 140, 200, 50, "Quit", RED, (255, 100, 100), 
                        lambda: "quit")
    
    back_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", BLUE, (100, 100, 255), 
                        lambda: "back")
    
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_state == PLAYING:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.jump()
                    elif event.key == pygame.K_ESCAPE:
                        game_state = MENU
                
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        # Reset game
                        score = 0
                        lives = 3
                        level = 1
                        game_state = PLAYING
                        
                        # Recreate level
                        all_sprites = pygame.sprite.Group()
                        platforms, coins, enemies = create_level(level)
                        all_sprites.add(platforms)
                        all_sprites.add(coins)
                        all_sprites.add(enemies)
                        player = Player()
                        all_sprites.add(player)
            
            # Handle button clicks
            if game_state == MENU:
                for button in [start_button, controls_button, quit_button]:
                    button.check_hover(mouse_pos)
                    action = button.handle_event(event)
                    if action == "start":
                        game_state = PLAYING
                    elif action == "controls":
                        game_state = CONTROLS
                    elif action == "quit":
                        running = False
            
            elif game_state == CONTROLS or game_state == GAME_OVER:
                back_button.check_hover(mouse_pos)
                action = back_button.handle_event(event)
                if action == "back":
                    game_state = MENU
        
        if game_state == PLAYING:
            # Get keyboard state for continuous movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
            
            # Check if all coins are collected
            if len(coins) == 0:
                level += 1
                # Create new level
                all_sprites = pygame.sprite.Group()
                platforms, coins, enemies = create_level(level)
                all_sprites.add(platforms)
                all_sprites.add(coins)
                all_sprites.add(enemies)
                player = Player()
                all_sprites.add(player)
            
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
        draw_background(level)
        
        # Draw sprites
        all_sprites.draw(screen)
        
        # Draw score, lives and level
        draw_text(f"Score: {score}", 36, WHITE, 100, 10)
        draw_text(f"Lives: {lives}", 36, WHITE, 700, 10)
        if game_state == PLAYING:
            draw_text(f"Level: {level}", 36, WHITE, SCREEN_WIDTH // 2, 10)
        
        # Draw game state screens
        if game_state == MENU:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            draw_text("ENHANCED PLATFORMER", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
            
            # Draw buttons
            start_button.draw(screen)
            controls_button.draw(screen)
            quit_button.draw(screen)
        
        elif game_state == CONTROLS:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 192))
            screen.blit(overlay, (0, 0))
            
            draw_text("CONTROLS", 64, WHITE, SCREEN_WIDTH // 2, 50)
            
            # Draw control instructions
            controls = [
                "Arrow Keys / A,D - Move Left/Right",
                "Space / Up / W - Jump",
                "ESC - Return to Menu",
                "",
                "Collect all coins to advance to next level",
                "Avoid enemies or lose a life",
                "Game ends when all lives are lost"
            ]
            
            for i, line in enumerate(controls):
                draw_text(line, 30, WHITE, SCREEN_WIDTH // 2, 150 + i * 40)
            
            # Draw back button
            back_button.draw(screen)
        
        elif game_state == GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            draw_text("GAME OVER", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            draw_text(f"Final Score: {score}", 48, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(f"Levels Completed: {level-1}", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text("Press ENTER to play again", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            
            # Draw back button
            back_button.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
