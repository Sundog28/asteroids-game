import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot

# Initialize pygame and window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

# Create sprite groups
updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

# Set class containers
Player.containers = updatable, drawable
Asteroid.containers = asteroids, updatable, drawable
Shot.containers = shots, updatable, drawable
AsteroidField.containers = updatable  # Not drawable

# Create game objects
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
asteroid_field = AsteroidField()

# Main game loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Time in seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all objects
    updatable.update(dt)

    # Check player-asteroid collisions
    for asteroid in asteroids:
        if player.collides_with(asteroid):
            print("Game over!")
            pygame.quit()
            sys.exit()

    # Check bullet-asteroid collisions
    for asteroid in asteroids:
        for shot in shots:
            if shot.collides_with(asteroid):
                asteroid.split()
                shot.kill()

    # Drawing
    screen.fill(BLACK)
    for sprite in drawable:
        sprite.draw(screen)
    pygame.display.flip()

pygame.quit()
