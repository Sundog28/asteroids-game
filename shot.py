# shot.py

import pygame
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((4, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 4, 10))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.angle = angle
        self.speed = 500

        self.velocity = pygame.Vector2(
            self.speed * -math.sin(math.radians(self.angle)),
            self.speed * -math.cos(math.radians(self.angle))
        )
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos

        if (self.pos.x < 0 or self.pos.x > SCREEN_WIDTH or
            self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT):
            self.kill()
