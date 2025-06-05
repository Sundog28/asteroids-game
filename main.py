import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from bomb import Bomb
from powerup import ShieldPowerUp, SpeedPowerUp
from explosion import Explosion
from ui import HUD

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
explosions = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bombs = pygame.sprite.Group()

# Player setup
player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
all_sprites.add(player)

# Asteroid field
asteroid_field = AsteroidField(asteroids, count=6)
all_sprites.add(asteroids)

# HUD
hud = HUD(font)

# Game variables
score = 0
lives = 3
invincible_timer = 0

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # seconds since last frame
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shot = Shot(player.pos, player.angle)
                shots.add(shot)
                all_sprites.add(shot)
            
            # Drop bomb
            if event.key == pygame.K_b:
                bomb = Bomb(player.pos)
                bombs.add(bomb)
                all_sprites.add(bomb)

    # Update sprites
    player.update(dt, keys)
    asteroids.update(dt)
    shots.update(dt)
    bombs.update(dt)
    powerups.update(dt)
    explosions.update(dt)

    # Bomb explosion handling
    for bomb in bombs.sprites():
        bomb_explosion = bomb.explode() if bomb.timer <= 0 else None
        if bomb_explosion:
            explosions.add(bomb_explosion)
            all_sprites.add(bomb_explosion)

    # Check shot collisions with asteroids
    for shot in shots:
        hit_asteroids = pygame.sprite.spritecollide(shot, asteroids, False, pygame.sprite.collide_mask)
        for asteroid in hit_asteroids:
            score += 10
            shots.remove(shot)
            all_sprites.remove(shot)
            shot.kill()
            # Split asteroid into smaller ones
            smaller_asteroids = asteroid.split()
            asteroids.remove(asteroid)
            all_sprites.remove(asteroid)
            asteroid.kill()
            for new_ast in smaller_asteroids:
                asteroids.add(new_ast)
                all_sprites.add(new_ast)
            # Explosion effect
            explosion = Explosion(asteroid.pos)
            explosions.add(explosion)
            all_sprites.add(explosion)

    # Player collisions with asteroids
    if invincible_timer <= 0:
        hit_by_asteroid = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_mask)
        if hit_by_asteroid:
            lives -= 1
            invincible_timer = 3  # 3 seconds of invincibility after hit
            player.respawn()
            if lives <= 0:
                print("Game Over!")
                running = False

    # Player collisions with powerups
    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in powerup_hits:
        powerup.apply(player)

    # Decrease invincibility timer
    if invincible_timer > 0:
        invincible_timer -= dt

    # Draw everything
    screen.fill((0, 0, 0))  # black background
    all_sprites.draw(screen)

    # Draw HUD
    hud.draw_score(screen, score)
    hud.draw_lives(screen, lives)

    pygame.display.flip()

pygame.quit()
sys.exit()
