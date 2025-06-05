# bomb.py

import pygame
from explosion import Explosion
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.timer = 3  # seconds before explosion

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.explode()

    def explode(self):
        # Create explosion and remove bomb
        explosion = Explosion(self.pos)
        self.kill()
        # You should add this explosion to your groups externally
        # Return explosion so main can add it to groups
        return explosion
