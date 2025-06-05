# player.py

import pygame
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.original_image = pygame.image.load("assets/ship.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 200  # degrees per second
        self.acceleration = 200  # pixels per second squared
        self.max_speed = 300
        self.friction = 0.99
        self.lives = 3
        self.respawn_timer = 0
        self.shield = False

    def update(self, dt, keys):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                self.vel = pygame.Vector2(0, 0)

        # Rotation
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed * dt
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed * dt

        # Acceleration
        if keys[pygame.K_UP]:
            direction = pygame.Vector2(
                -math.sin(math.radians(self.angle)),
                -math.cos(math.radians(self.angle))
            )
            self.vel += direction * self.acceleration * dt

        # Friction
        self.vel *= self.friction

        # Limit speed
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Move
        self.pos += self.vel * dt

        # Screen wrap
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        elif self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT
        elif self.pos.y > SCREEN_HEIGHT:
            self.pos.y = 0

        # Rotate image and update rect
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def respawn(self):
        self.lives -= 1
        self.respawn_timer = 3  # seconds invulnerability
        self.pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel = pygame.Vector2(0, 0)
