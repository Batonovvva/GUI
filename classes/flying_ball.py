import math
import pygame
from logic import settings


class FlyingBall:
    def __init__(self, x, y, dx, dy, color, speed=None, radius=None, ball_type='normal'):
        self.pos = [float(x), float(y)]
        mag = math.hypot(dx, dy)
        if mag == 0:
            self.dx, self.dy = 1.0, 0.0
        else:
            self.dx, self.dy = dx / mag, dy / mag

        self.speed = speed if speed is not None else settings.SHOT_SPEED
        self.radius = radius if radius is not None else settings.BALL_RADIUS
        self.color = color
        self.type = ball_type
        self.alive = True

    def update(self, dt):
        # dt — секунды
        self.pos[0] += self.dx * self.speed * dt
        self.pos[1] += self.dy * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))
        pygame.draw.circle(screen, settings.BLACK, (int(self.pos[0]), int(self.pos[1])), int(self.radius), 1)

    def is_offscreen(self):
        x, y = self.pos
        return x < -self.radius or x > settings.WIDTH + self.radius or y < -self.radius or y > settings.HEIGHT + self.radius
