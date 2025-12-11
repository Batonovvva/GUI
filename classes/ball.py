import pygame
from logic import spiral, settings


class Ball:
    TYPE_NORMAL = 'normal'
    TYPE_SKULL = 'skull'

    def __init__(self, color, t, ball_type='normal'):
        self.color = color
        self.type = ball_type
        self.t = t
        self.radius = settings.BALL_RADIUS
        self.pos = self.calculate_position()

    def pos(self):
        return settings.get_spiral_position(self.t)

    def calculate_position(self):
        return spiral.get_position(self.t)
    
    def update(self, dt, speed=None):
        if speed is None:
            speed = settings.SPIRAL_SPEED
        
        self.t += dt * speed
        self.pos = self.calculate_position()
    
    def draw(self, screen):
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), self.radius, 2)
        
        if self.type == 'normal':
            pygame.draw.circle(screen, self.color, (x, y), self.radius)
            pygame.draw.circle(screen, settings.BLACK, (x, y), self.radius, 2)
        
        elif self.type == 'skull':
            pygame.draw.circle(screen, settings.SKULL_COLOR, (x, y), self.radius)
            pygame.draw.circle(screen, settings.WHITE, (x, y), self.radius, 2)

            offset = self.radius // 2
            pygame.draw.line(
                screen, 
                settings.RED,
                (x - offset, y - offset),
                (x + offset, y + offset),
                3
            )
            pygame.draw.line(
                screen,
                settings.RED,
                (x - offset, y + offset),
                (x + offset, y - offset),
                3
            )
    
    def distance_to(self, other):
        if isinstance(other, Ball):
            other_pos = other.pos
        else:
            other_pos = other
        
        dx = self.pos[0] - other_pos[0]
        dy = self.pos[1] - other_pos[1]
        return (dx**2 + dy**2) ** 0.5
    
    def is_at_end(self):
        r = settings.SPIRAL_START_RADIUS - self.t * settings.SPIRAL_TIGHTNESS
        return r <= settings.SPIRAL_END_RADIUS
