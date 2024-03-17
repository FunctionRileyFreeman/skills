import pygame
import sys
import random
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30

# Colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)  # Red square player
HEALTH_BAR_COLOR = (0, 255, 0)
DAMAGE_BAR_COLOR = (255, 0, 0)
XP_BAR_COLOR = (0, 0, 255)
WALL_COLOR = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ecosystem RPG")

# Player stats
player_health = 100
player_attack = 10
player_defense = 5
player_inventory = [{"name": "Sword", "attack_power": 5, "equipped": True}]  # List to store items

# Player position and size
player_rect = pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 30, 30)  # Random starting position

# Player speed
player_speed = 5

# Sword swing range
sword_range = 20

# Player XP and level
player_xp = 0
player_level = 1
xp_to_next_level = 100

# Create maze walls
def generate_random_walls():
    walls = []
    num_walls = random.randint(5, 10)  # Adjust the number of walls as needed

    for _ in range(num_walls):
        wall_width = random.randint(50, 150)  # Adjust the width as needed
        wall_height = random.randint(50, 150)  # Adjust the height as needed
        wall_x = random.randint(0, WIDTH - wall_width)
        wall_y = random.randint(0, HEIGHT - wall_height)

        wall = pygame.Rect(wall_x, wall_y, wall_width, wall_height)
        walls.append(wall)

    return walls

maze_walls = generate_random_walls()

# Create enemies
enemy_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 255)]
enemies = []

for _ in range(5):
    enemy_color = random.choice(enemy_colors)
    enemy_radius = 20  # Adjust the radius as needed
    enemy_center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    enemy_health = random.randint(10, 30)
    enemies.append({"color": enemy_color, "center": enemy_center, "radius": enemy_radius,
                    "health": enemy_health, "max_health": enemy_health, "attack": 2, "xp": enemy_health})

# Create a clock to control frame rate
clock = pygame.time.Clock()

# Font for HUD
font = pygame.font.Font(None, 36)

# Health regeneration
health_regeneration_timer = 0  # Timer for health regeneration
health_regeneration_interval = 2 * FPS  # Regenerate health every 2 seconds

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Store the previous player position
    player_rect_old_x, player_rect_old_y = player_rect.x, player_rect.y

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += player_speed

    # Handle wall collisions
    for wall in maze_walls:
        if player_rect.colliderect(wall):
            player_rect.x, player_rect.y = player_rect_old_x, player_rect_old_y

    # Handle sword swing
    for enemy in enemies:
        enemy_center = enemy["center"]
        player_center = (player_rect.centerx, player_rect.centery)
        distance = math.sqrt((player_center[0] - enemy_center[0]) ** 2 + (player_center[1] - enemy_center[1]) ** 2)
        if distance <= sword_range and pygame.mouse.get_pressed()[0]:
            # Swing sword and deal damage
            if any(item["name"] == "Sword" and item["equipped"] for item in player_inventory):
                sword_damage = next(item["attack_power"] for item in player_inventory if item["name"] == "Sword")
                enemy["health"] -= sword_damage

                if enemy["health"] <= 0:
                    # Gain XP from defeating enemy
                    player_xp += enemy["xp"]

    # Check for level up
    if player_xp >= xp_to_next_level:
        player_level += 1
        xp_to_next_level *= 2  # Double XP required for next level

    # Update game logic
    for enemy in enemies[:]:
        if enemy["health"] <= 0:
            enemies.remove(enemy)

    # Health regeneration
    health_regeneration_timer += 1
    if health_regeneration_timer >= health_regeneration_interval:
        player_health = min(player_health + 5, 100)
        health_regeneration_timer = 0

    # Draw the game elements
    screen.fill(GREEN)  # Fill the background with green

    # Draw maze walls
    for wall in maze_walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

    # Draw the square player
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Draw circular enemies and health bars
    for enemy in enemies:
        pygame.draw.circle(screen, enemy["color"], enemy["center"], enemy["radius"])

        # Calculate health bar position and size
        health_bar_width = 2 * enemy["radius"]
        health_bar_height = 5
        health_bar_x = enemy["center"][0] - enemy["radius"]
        health_bar_y = enemy["center"][1] + enemy["radius"] + 5

        # Draw the health bar background (gray)
        pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Calculate health bar (green) based on enemy's health percentage
        health_percentage = max(enemy["health"] / enemy["max_health"], 0)
        health_bar_length = int(health_percentage * health_bar_width)
        pygame.draw.rect(screen, HEALTH_BAR_COLOR, (health_bar_x, health_bar_y, health_bar_length, health_bar_height))

    # Draw the XP progress bar
    xp_bar_width = WIDTH - 20
    xp_bar_height = 20
    xp_bar_x = 10
    xp_bar_y = HEIGHT - 30

    # Draw the XP bar background (gray)
    pygame.draw.rect(screen, WHITE, (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height))

    # Calculate XP bar (blue) based on player's XP progress
    xp_percentage = min(player_xp / xp_to_next_level, 1.0)
    xp_bar_length = int(xp_percentage * xp_bar_width)
    pygame.draw.rect(screen, XP_BAR_COLOR, (xp_bar_x, xp_bar_y, xp_bar_length, xp_bar_height))

    # Draw the HUD
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    attack_text = font.render(f"Attack: {player_attack}", True, WHITE)
    defense_text = font.render(f"Defense: {player_defense}", True, WHITE)
    level_text = font.render(f"Level: {player_level}", True, WHITE)

    screen.blit(health_text, (10, 10))
    screen.blit(attack_text, (10, 50))
    screen.blit(defense_text, (10, 90))
    screen.blit(level_text, (10, 130))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
