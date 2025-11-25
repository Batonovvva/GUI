import math
import random
from logic import settings


def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.hypot(dx, dy)


def random_ball_color(used_colors=None):
    if used_colors is None:
        used_colors = settings.BALL_COLORS
    return random.choice(used_colors)

def polar_to_cartesian(r, theta, center=settings.SPIRAL_CENTER_X, center_y=settings.SPIRAL_CENTER_Y):
    x = center + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    return (x, y)


def cartesian_to_polar(x, y, center=settings.SPIRAL_CENTER_X, center_y=settings.SPIRAL_CENTER_Y):
    dx = x - center
    dy = y - center_y
    r = math.hypot(dx, dy)
    theta = math.atan2(dy, dx)
    return (r, theta)
