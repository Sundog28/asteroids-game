import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()  # Always remove current asteroid

        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Small asteroids do not split further

        # New radius for smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Generate two random angles to split
        angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(angle) * 1.2
        vel2 = self.velocity.rotate(-angle) * 1.2

        # Create two new asteroids at the same position with new velocity and radius
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = vel1

        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        a2.velocity = vel2
