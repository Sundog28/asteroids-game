# explosion.py

import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = []
        for size in range(20, 70, 10):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 165, 0, 255 - size * 3), (size//2, size//2), size//2)
            self.frames.append(surf)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer > 0.1:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=self.rect.center)
