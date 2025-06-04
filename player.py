import pygame
from constants import *
from circleshape import CircleShape  # Assuming you have this base class

class Player(CircleShape):
    containers = ()  # This will be set externally to groups

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def rotate(self, dt, direction=1):
        # direction: 1 for right, -1 for left
        self.rotation += PLAYER_TURN_SPEED * dt * direction

    def move(self, dt, forward=True):
        direction_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        if not forward:
            direction_vector = -direction_vector
        self.position += direction_vector * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_cooldown > 0:
            return  # still cooling down, cannot shoot

        # Create a new shot at the player's position moving forward
        from shot import Shot  # Import here to avoid circular imports
        shot = Shot(self.position.x, self.position.y)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED

        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt, direction=-1)
        if keys[pygame.K_d]:
            self.rotate(dt, direction=1)
        if keys[pygame.K_w]:
            self.move(dt, forward=True)
        if keys[pygame.K_s]:
            self.move(dt, forward=False)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

