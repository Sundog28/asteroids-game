# asteroid.py

import pygame
import random
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = size  # radius approx
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
        self.angle = 0
        self.angular_velocity = random.uniform(-90, 90)
        self.create_image()

    def create_image(self):
        # Create lumpy asteroid shape polygon
        count = 8
        radius = self.size
        points = []
        for i in range(count):
            angle_deg = i * (360 / count) + random.uniform(-10, 10)
            length = radius + random.uniform(-radius * 0.4, radius * 0.4)
            x = radius + length * math.cos(math.radians(angle_deg))
            y = radius + length * math.sin(math.radians(angle_deg))
            points.append((x, y))
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (200, 200, 200), points)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.pos += self.velocity * dt
        self.angle += self.angular_velocity * dt

        # Screen wrap
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        elif self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT
        elif self.pos.y > SCREEN_HEIGHT:
            self.pos.y = 0

        # Rotate image
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def split(self):
        if self.size > 20:
            new_size = self.size // 2
            asteroids = []
            for _ in range(2):
                a = Asteroid(self.pos.x, self.pos.y, new_size)
                asteroids.append(a)
            return asteroids
        else:
            return []
