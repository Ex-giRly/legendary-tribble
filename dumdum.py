import pygame 
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(pygame.image.load("player_ship-removebg-preview.png"))

background = pygame.image.load('download.webp')
player_ing = pygame.image.load('player_ship-removebg-preview.png')
enemy_ing =pygame.transform.scale(pygame.image.load('Enemy_spaceship-removebg-preview.png'), (20,20))
bullet_ing = pygame.image.load('bullet-removebg-preview (1).png')

player = {"x":370, "y":380, "dx":0}

bullet = {"x":0, "y":380, "dy":0, "state":"ready", "speed":10}

enemies = []
for _ in range(6):
    enemies.append({
        "x": random.randint(0, WIDTH - 64),
        "y": random.randint(50, 150),
        "dx": 4,
        "dy": 40
    })
score = 0
font = pygame.font.Font(None, 32)
over_font = pygame.font.Font(None, 64)


def draw_player():
    screen.blit(player_ing, (player["x"], player["y"]))

def draw_enemy(e):
    screen.blit(enemy_ing, (e["x"], e["y"]))

def fire_bullet():
    bullet["state"] = "fire"
    screen.blit(bullet_ing, (bullet["x"] + 16, bullet["y"] +10))

def is_collision(e):
    return math.hypot(e["x"], e["y"] - bullet["y"] )
    
def show_score():
    text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text, (10,10))

def game_over():
    text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(text, (200,250))


running = True
while running:
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player["dx"] = -5

            if event.key == pygame.K_RIGHT:
                player["dx"] = 5
            if event.key == pygame.K_SPACE  and bullet["state"] == "ready":
                bullet["x"]  = player["x"]
                bullet["y"]  = player["y"] 
                bullet["state"]  = "fire"
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player["dx"] - 0

    player["x"] += player["dx"]
    player["x"] = max(0, min(player["x"], WIDTH - 64))

    # Enemies
    for e in enemies:
        if e["y"] > 340:
            for enemy in enemies:
                enemy["y"] = 2000
            game_over()
            break

        e["x"] += e["dx"]
        if e["x"] <= 0 or e["x"] >= WIDTH - 64:
            e["dx"] *= -1
            e["y"] += e["dy"]

        if bullet["state"] == "fire" and is_collision(e):
            bullet["state"] = "ready"
            score += 1
            e["x"] = random.randint(0, WIDTH - 64)
            e["y"] = random.randint(50, 150)

        draw_enemy(e)

    # Bullet movement
    if bullet["state"] == "fire":
        fire_bullet()
        bullet["y"] -= bullet["speed"]
        if bullet["y"] <= 0:
            bullet["state"] = "ready"

    draw_player()
    show_score()
    pygame.display.update()