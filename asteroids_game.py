import pygame
import random
import math
import os

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Game")

# Load assets paths
ASSETS_DIR = "assets"
BACKGROUND_IMG = os.path.join(ASSETS_DIR, "background.png")
SHIP_IMG = os.path.join(ASSETS_DIR, "ship.png")
ASTEROID_IMG = os.path.join(ASSETS_DIR, "asteroid.png")
BULLET_IMG = os.path.join(ASSETS_DIR, "bullet.png")
BOMB_IMG = os.path.join(ASSETS_DIR, "bomb.png")

# Load sounds
SHOOT_SOUND = os.path.join(ASSETS_DIR, "shoot.wav")
BOMB_SOUND = os.path.join(ASSETS_DIR, "bomb.wav")
EXPLOSION_SOUND = os.path.join(ASSETS_DIR, "explosion.wav")
BG_MUSIC = os.path.join(ASSETS_DIR, "background.mp3")

# Game constants
FPS = 60
MAX_BOMBS = 3

# Utility functions
def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

def wrap_position(pos):
    x, y = pos
    x %= WIDTH
    y %= HEIGHT
    return x, y

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Classes
class Ship:
    def __init__(self):
        self.image = load_image(SHIP_IMG, (50, 50))
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 5
        self.acceleration = 0.2
        self.friction = 0.98
        self.lives = 3
        self.speed_powerup = False
        self.shield_powerup = False
        self.shield_timer = 0
        self.speed_timer = 0

    def rotate(self, direction):
        self.angle += self.rotation_speed * direction

    def accelerate(self):
        radians = math.radians(self.angle)
        force = pygame.Vector2(math.cos(radians), -math.sin(radians)) * self.acceleration
        self.velocity += force

    def update(self):
        self.position += self.velocity
        self.position = pygame.Vector2(wrap_position(self.position))
        self.velocity *= self.friction
        # Handle powerup timers
        if self.shield_powerup:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_powerup = False
        if self.speed_powerup:
            self.speed_timer -= 1
            if self.speed_timer <= 0:
                self.speed_powerup = False
                self.acceleration = 0.2

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=self.position)
        surface.blit(rotated_image, rect.topleft)
        if self.shield_powerup:
            pygame.draw.circle(surface, (0, 150, 255), (int(self.position.x), int(self.position.y)), 40, 3)

    def hit(self):
        if self.shield_powerup:
            # Shield absorbs hit
            self.shield_powerup = False
        else:
            self.lives -= 1

    def activate_shield(self, duration=300):
        self.shield_powerup = True
        self.shield_timer = duration

    def activate_speed(self, duration=300):
        self.speed_powerup = True
        self.speed_timer = duration
        self.acceleration = 0.5

class Asteroid:
    def __init__(self, position=None, size=3):
        self.size = size  # 3=big, 2=medium, 1=small
        scale = {3: 80, 2: 50, 1: 30}[size]
        self.image = load_image(ASTEROID_IMG, (scale, scale))
        if position:
            self.position = pygame.Vector2(position)
        else:
            # Spawn randomly at edges
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                self.position = pygame.Vector2(random.uniform(0, WIDTH), 0)
            elif edge == 'bottom':
                self.position = pygame.Vector2(random.uniform(0, WIDTH), HEIGHT)
            elif edge == 'left':
                self.position = pygame.Vector2(0, random.uniform(0, HEIGHT))
            else:
                self.position = pygame.Vector2(WIDTH, random.uniform(0, HEIGHT))
        angle = random.uniform(0, 360)
        speed = random.uniform(1, 3) / size
        self.velocity = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle))) * speed
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position += self.velocity
        self.position = pygame.Vector2(wrap_position(self.position))
        self.rect.center = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Bullet:
    def __init__(self, position, angle):
        self.image = load_image(BULLET_IMG, (10, 10))
        self.position = pygame.Vector2(position)
        self.speed = 10
        radians = math.radians(angle)
        self.velocity = pygame.Vector2(math.cos(radians), -math.sin(radians)) * self.speed
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def is_off_screen(self):
        x, y = self.position
        return x < 0 or x > WIDTH or y < 0 or y > HEIGHT

class Bomb:
    def __init__(self, position):
        self.image = load_image(BOMB_IMG, (20, 20))
        self.position = pygame.Vector2(position)
        self.timer = 60  # frames until explosion
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.timer -= 1

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def exploded(self):
        return self.timer <= 0

class PowerUp:
    TYPES = ['shield', 'speed']
    def __init__(self):
        self.type = random.choice(PowerUp.TYPES)
        self.position = pygame.Vector2(random.uniform(50, WIDTH - 50), random.uniform(50, HEIGHT - 50))
        self.image = pygame.Surface((30,30), pygame.SRCALPHA)
        color = (0,150,255) if self.type == 'shield' else (255, 200, 0)
        pygame.draw.circle(self.image, color, (15,15), 15)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Initialize assets
background = load_image(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Load sounds
shoot_sound = pygame.mixer.Sound(SHOOT_SOUND)
bomb_sound = pygame.mixer.Sound(BOMB_SOUND)
explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND)

# Play background music looped
pygame.mixer.music.load(BG_MUSIC)
pygame.mixer.music.play(-1)

def main():
    clock = pygame.time.Clock()

    ship = Ship()
    asteroids = [Asteroid() for _ in range(6)]
    bullets = []
    bombs = []
    powerups = []

    score = 0
    bomb_count = MAX_BOMBS

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Ship controls
        if keys[pygame.K_LEFT]:
            ship.rotate(1)
        if keys[pygame.K_RIGHT]:
            ship.rotate(-1)
        if keys[pygame.K_UP]:
            ship.accelerate()
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullet = Bullet(ship.position, ship.angle)
                bullets.append(bullet)
                shoot_sound.play()
        if keys[pygame.K_b]:
            if bomb_count > 0:
                bomb = Bomb(ship.position)
                bombs.append(bomb)
                bomb_sound.play()
                bomb_count -= 1

        # Update game objects
        ship.update()
        for asteroid in asteroids:
            asteroid.update()
        for bullet in bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                bullets.remove(bullet)

        for bomb in bombs[:]:
            bomb.update()
            if bomb.exploded():
                # Explosion logic: destroy asteroids within radius
                explosion_radius = 100
                for asteroid in asteroids[:]:
                    if distance(asteroid.position, bomb.position) < explosion_radius:
                        asteroids.remove(asteroid)
                        score += 10 * asteroid.size
                        explosion_sound.play()
                bombs.remove(bomb)

        # Collision detection: bullets and asteroids
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet.rect.colliderect(asteroid.rect):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10 * asteroid.size
                    explosion_sound.play()
                    # Split asteroid if size > 1
                    if asteroid.size > 1:
                        for _ in range(2):
                            new_asteroid = Asteroid(position=asteroid.position, size=asteroid.size -1)
                            asteroids.append(new_asteroid)
                    break

        # Collision detection: ship and asteroids
        for asteroid in asteroids:
            if ship.position.distance_to(asteroid.position) < 40:
                ship.hit()
                asteroids.remove(asteroid)
                explosion_sound.play()
                if ship.lives <= 0:
                    running = False

        # Power-up spawn chance
        if random.randint(1, 1000) == 1 and len(powerups) < 3:
            powerups.append(PowerUp())

        # Power-up pickup
        for powerup in powerups[:]:
            if ship.position.distance_to(powerup.position) < 40:
                if powerup.type == 'shield':
                    ship.activate_shield()
                elif powerup.type == 'speed':
                    ship.activate_speed()
                powerups.remove(powerup)

        # Draw everything
        screen.blit(background, (0, 0))
        ship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for bomb in bombs:
            bomb.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        # UI: score, lives, bombs, powerups
        font = pygame.font.SysFont("arial", 20)
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        lives_text = font.render(f"Lives: {ship.lives}", True, (255,255,255))
        bombs_text = font.render(f"Bombs: {bomb_count}", True, (255,255,255))
        shield_text = font.render(f"Shield: {'ON' if ship.shield_powerup else 'OFF'}", True, (0,150,255))
        speed_text = font.render(f"Speed: {'ON' if ship.speed_powerup else 'OFF'}", True, (255,200,0))

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 30))
        screen.blit(bombs_text, (10, 50))
        screen.blit(shield_text, (10, 70))
        screen.blit(speed_text, (10, 90))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
