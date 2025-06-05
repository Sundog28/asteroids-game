# asteroidfield.py

import random
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class AsteroidField:
    def __init__(self, group, count=5):
        self.group = group
        self.count = count
        self.spawn_asteroids()

    def spawn_asteroids(self):
        for _ in range(self.count):
            x = random.choice([random.randint(0, 50), random.randint(SCREEN_WIDTH-50, SCREEN_WIDTH)])
            y = random.choice([random.randint(0, 50), random.randint(SCREEN_HEIGHT-50, SCREEN_HEIGHT)])
            size = random.choice([40, 50, 60])
            asteroid = Asteroid(x, y, size)
            self.group.add(asteroid)

    def update(self, dt):
        for asteroid in self.group.sprites():
            asteroid.update(dt)
