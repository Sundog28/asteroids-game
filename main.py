import os
import sys
import pygame
import random
import math
import time

print("Starting game...")
time.sleep(2)

pygame.init()
pygame.mixer.init()

# Paths
ASSETS_DIR = "assets"
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Load assets
BACKGROUND_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "background.png"))
SHIP_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "ship.png"))
ASTEROID_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "asteroid.png"))
BULLET_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "bullet.png"))
BOMB_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "bomb.png"))

SHOOT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "shoot.wav"))
BOMB_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "bomb.wav"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "explosion.wav"))

pygame.mixer.music.load(os.path.join(ASSETS_DIR, "background.wav"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # loop

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

# Utility functions
def wrap_position(pos):
    x, y = pos
    return (x % SCREEN_WIDTH, y % SCREEN_HEIGHT)

def angle_to_vector(angle):
    return math.cos(angle), math.sin(angle)

def load_image_centered(image, pos):
    rect = image.get_rect(center=pos)
    return rect

# Classes
class Player:
    def __init__(self):
        self.image = SHIP_IMG
        self.position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 0
        self.acceleration = 0
        self.lives = 3
        self.respawn_timer = 0
        self.shield = 0
        self.speed_powerup_timer = 0
        self.bomb_ammo = 3

    def update(self, dt):
        self.angle += self.rotation_speed * dt
        # Apply acceleration in direction of angle
        if self.acceleration:
            forward = pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))
            speed = 300 if self.speed_powerup_timer <= 0 else 500
            self.velocity += forward * self.acceleration * speed * dt
        # Apply friction
        self.velocity *= 0.99
        self.position += self.velocity * dt
        self.position = pygame.math.Vector2(wrap_position(self.position))
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
        if self.speed_powerup_timer > 0:
            self.speed_powerup_timer -= dt
        if self.shield > 0:
            self.shield -= dt

    def draw(self, surf):
        rotated = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        rect = rotated.get_rect(center=self.position)
        surf.blit(rotated, rect)
        if self.shield > 0:
            pygame.draw.circle(surf, (0, 200, 255), (int(self.position.x), int(self.position.y)), 40, 3)

    def hit(self):
        if self.shield > 0:
            self.shield = 0
        else:
            self.lives -= 1
            self.respawn_timer = 3
            self.position = pygame.math.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            self.velocity = pygame.math.Vector2(0, 0)

class Asteroid:
    def __init__(self):
        self.image = ASTEROID_IMG
        self.position = pygame.math.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(30, 100)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.rotation = random.uniform(-1, 1)
        self.angle = 0
        self.radius = 40

    def update(self, dt):
        self.position += self.velocity * dt
        self.position = pygame.math.Vector2(wrap_position(self.position))
        self.angle += self.rotation * dt

    def draw(self, surf):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=self.position)
        surf.blit(rotated, rect)

    def get_hitbox(self):
        return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius,
                           self.radius * 2, self.radius * 2)

class Bullet:
    def __init__(self, pos, angle):
        self.image = BULLET_IMG
        self.position = pygame.math.Vector2(pos)
        speed = 700
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.radius = 5
        self.lifetime = 2  # seconds

    def update(self, dt):
        self.position += self.velocity * dt
        self.position = pygame.math.Vector2(wrap_position(self.position))
        self.lifetime -= dt

    def draw(self, surf):
        rect = self.image.get_rect(center=self.position)
        surf.blit(self.image, rect)

    def is_alive(self):
        return self.lifetime > 0

class Bomb:
    def __init__(self, pos):
        self.image = BOMB_IMG
        self.position = pygame.math.Vector2(pos)
        self.radius = 20
        self.timer = 3  # seconds before explosion

    def update(self, dt):
        self.timer -= dt

    def draw(self, surf):
        rect = self.image.get_rect(center=self.position)
        surf.blit(self.image, rect)

    def explode(self):
        # Returns True if bomb exploded
        return self.timer <= 0

# Game variables
player = Player()
asteroids = [Asteroid() for _ in range(5)]
bullets = []
bombs = []
score = 0
font = pygame.font.SysFont("Arial", 24)

def check_collision(obj1_pos, obj1_radius, obj2_pos, obj2_radius):
    dist = obj1_pos.distance_to(obj2_pos)
    return dist < (obj1_radius + obj2_radius)

def reset_game():
    global asteroids, bullets, bombs, score
    player.lives = 3
    player.position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.velocity = pygame.math.Vector2(0, 0)
    player.respawn_timer = 0
    player.shield = 0
    player.speed_powerup_timer = 0
    player.bomb_ammo = 3
    asteroids = [Asteroid() for _ in range(5)]
    bullets = []
    bombs = []
    score = 0

running = True
while running:
    dt = clock.tick(60) / 1000  # seconds elapsed since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rotation_speed = -3
    elif keys[pygame.K_RIGHT]:
        player.rotation_speed = 3
    else:
        player.rotation_speed = 0

    if keys[pygame.K_UP]:
        player.acceleration = 1
    else:
        player.acceleration = 0

    if keys[pygame.K_SPACE]:
        if player.respawn_timer <= 0:
            if len(bullets) < 5:
                SHOOT_SOUND.play()
                bullets.append(Bullet(player.position, player.angle))

    if keys[pygame.K_b]:
        if player.bomb_ammo > 0:
            BOMB_SOUND.play()
            bombs.append(Bomb(player.position))
            player.bomb_ammo -= 1

    # Update game objects
    player.update(dt)

    for asteroid in asteroids:
        asteroid.update(dt)

    for bullet in bullets[:]:
        bullet.update(dt)
        if not bullet.is_alive():
            bullets.remove(bullet)

    for bomb in bombs[:]:
        bomb.update(dt)
        if bomb.explode():
            EXPLOSION_SOUND.play()
            # Destroy all asteroids near bomb
            asteroids = [a for a in asteroids if not check_collision(a.position, a.radius, bomb.position, bomb.radius + 50)]
            bombs.remove(bomb)
            score += 10

    # Collision: bullets vs asteroids
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if check_collision(bullet.position, bullet.radius, asteroid.position, asteroid.radius):
                EXPLOSION_SOUND.play()
                try:
                    bullets.remove(bullet)
                except:
                    pass
                try:
                    asteroids.remove(asteroid)
                except:
                    pass
                score += 5
                # Spawn smaller asteroids if big ones? For simplicity, respawn new asteroid
                asteroids.append(Asteroid())
                break

    # Collision: player vs asteroids
    if player.respawn_timer <= 0:
        for asteroid in asteroids:
            if check_collision(player.position, 20, asteroid.position, asteroid.radius):
                player.hit()
                EXPLOSION_SOUND.play()
                if player.lives <= 0:
                    reset_game()
                break

    # Drawing
    screen.blit(BACKGROUND_IMG, (0,0))
    player.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for bomb in bombs:
        bomb.draw(screen)

    # UI
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    lives_text = font.render(f"Lives: {player.lives}", True, (255,255,255))
    bombs_text = font.render(f"Bombs: {player.bomb_ammo}", True, (255,255,255))
    screen.blit(score_text, (10,10))
    screen.blit(lives_text, (10,40))
    screen.blit(bombs_text, (10,70))

    pygame.display.flip()

pygame.quit()
sys.exit()
