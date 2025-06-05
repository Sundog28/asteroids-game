# powerup.py

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.velocity = pygame.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))

    def update(self, dt):
        self.pos += self.velocity * dt
        # screen wrap
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        elif self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = SCREEN_HEIGHT
        elif self.pos.y > SCREEN_HEIGHT:
            self.pos.y = 0
        self.rect.center = self.pos

class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.circle(self.image, (0, 0, 255), (10, 10), 10)

class SpeedPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.circle(self.image, (0, 255, 0), (10, 10), 10)

class Bomb(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        pygame.draw.circle(self.image, (255, 0, 0), (10, 10), 10)
