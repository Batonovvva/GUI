import pygame
import math
import random
from logic import settings
from classes.flying_ball import FlyingBall
from logic.settings import BALL_RADIUS, SHOT_SPEED

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
        self._last_shot_time = 0.0
        self.cooldown_base = 0.8          # базовый кулдаун (можешь менять)
        self.cooldown_multiplier = 1.0

        self.shoot_speed_multiplier = 1.0
        self.burst_shoot_count = 1  # обычный выстрел по умолчанию
        self.burst_angle_spread = math.radians(10)

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

    def can_shoot(self, now_time: float = None):
        if now_time is None:
            now_time = pygame.time.get_ticks() / 1000.0
        return (now_time - self._last_shot_time) >= (self.cooldown_base * self.cooldown_multiplier)

    def shoot(self, aim_pos=None):
        if not self.can_shoot():
            return []

        if aim_pos is not None:
            self.aim_at(aim_pos)

        x, y = self.pos
        angle = self.angle

        balls_to_shoot = getattr(self, "burst_shoot_count", 1)  # 1 или бонус
        created_balls = []

        for i in range(balls_to_shoot):
            spread = 0.05  # радианы, угол расхождения
            current_angle = angle + (i - balls_to_shoot//2) * spread
            dx = math.cos(current_angle)
            dy = math.sin(current_angle)

            speed_multiplier = getattr(self, "shoot_speed_multiplier", 1.0)
            flying = FlyingBall(
                x=x, y=y, dx=dx, dy=dy,
                color=self.current_ball_color,
                speed=settings.SHOT_SPEED * speed_multiplier,
                radius=settings.BALL_RADIUS,
                ball_type='normal'  # <-- исправлено
            )
            created_balls.append(flying)

        self.current_ball_color = self.next_ball_color
        self.next_ball_color = random.choice(settings.BALL_COLORS)
        self.shot_cooldown = self.shot_cooldown_time

        return created_balls



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
