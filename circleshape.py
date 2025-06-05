# circleshape.py

import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, pos, radius, color=(255, 255, 255)):
        super().__init__()
        diameter = radius * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.radius = radius

    def update(self, dt):
        pass  # Add movement or behavior if needed
