import pygame
import math
import random
from logic import settings
from classes.flying_ball import FlyingBall


class Frog:
    def __init__(self):
        self.pos = (settings.FROG_X, settings.FROG_Y)
        self.angle = 0.0
        self.target_angle = 0.0
        self.shot_cooldown = 0.0
        self.shot_cooldown_time = 0.2
        self.current_ball_color = random.choice(settings.BALL_COLORS)
        self.next_ball_color = random.choice(settings.BALL_COLORS)
        self.radius = settings.FROG_RADIUS

    def rotate(self, direction):
        step = math.radians(settings.FROG_ROTATION_SPEED) * direction
        self.target_angle += step

    def aim_at(self, target_pos):
        dx = target_pos[0] - self.pos[0]
        dy = target_pos[1] - self.pos[1]
        self.target_angle = math.atan2(dy, dx)

    def update(self, dt):
        if self.shot_cooldown > 0:
            self.shot_cooldown = max(0.0, self.shot_cooldown - dt)
        # плавный поворот
        angle_diff = (self.target_angle - self.angle)
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi
        max_step = math.radians(settings.FROG_ROTATION_SPEED) * dt * 5.0
        if abs(angle_diff) > max_step:
            self.angle += max_step if angle_diff > 0 else -max_step
        else:
            self.angle = self.target_angle

    def can_shoot(self):
        return self.shot_cooldown <= 0.0

    def shoot(self, aim_pos=None):
        if not self.can_shoot():
            return None

        if aim_pos is not None:
            self.aim_at(aim_pos)

        x, y = self.pos
        angle = self.angle
        dx = math.cos(angle)
        dy = math.sin(angle)

        flying = FlyingBall(x=x, y=y, dx=dx, dy=dy, color=self.current_ball_color,
                            speed=settings.SHOT_SPEED, radius=settings.BALL_RADIUS, ball_type=FlyingBall)

        self.current_ball_color = self.next_ball_color
        self.next_ball_color = random.choice(settings.BALL_COLORS)


        self.shot_cooldown = self.shot_cooldown_time

        return flying

    def draw(self, screen):
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(screen, settings.GREEN, (x, y), self.radius)
        pygame.draw.circle(screen, settings.BLACK, (x, y), self.radius, 2)
        aim_length = self.radius * 2
        end_x = x + aim_length * math.cos(self.angle)
        end_y = y + aim_length * math.sin(self.angle)
        pygame.draw.line(screen, settings.WHITE, (x, y), (end_x, end_y), 3)
        pygame.draw.circle(screen, self.current_ball_color, (x, y - self.radius - 10), self.radius // 2)
        pygame.draw.circle(screen, settings.BLACK, (x, y - self.radius - 10), self.radius // 2, 1)
        pygame.draw.circle(screen, self.next_ball_color, (x + self.radius + 12, y - self.radius - 10), self.radius // 2)
        pygame.draw.circle(screen, settings.BLACK, (x + self.radius + 12, y - self.radius - 10), self.radius // 2, 1)
