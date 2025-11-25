import math
from logic import settings


def get_radius(t):
    r = settings.SPIRAL_START_RADIUS - settings.SPIRAL_TIGHTNESS * t
    return max(r, 0.0)

def get_angle(t):
    return 0.2 * t

def get_position(t):
    r = get_radius(t)
    theta = get_angle(t)
    x = settings.SPIRAL_CENTER_X + r * math.cos(theta)
    y = settings.SPIRAL_CENTER_Y + r * math.sin(theta)
    return (x, y)

def distance_between_t(t1, t2):
    x1, y1 = get_position(t1)
    x2, y2 = get_position(t2)
    return math.hypot(x2 - x1, y2 - y1)

def find_t_at_distance(start_t, distance, forward=True, tol=0.5, max_iter=200):
    step = 1.0 if forward else -1.0
    current_t = start_t
    iter_count = 0

    while iter_count < max_iter:
        test_t = current_t + step
        cur_dist = distance_between_t(start_t, test_t)
        if abs(cur_dist - distance) <= tol:
            return test_t
        if cur_dist < distance:
            current_t = test_t
        else:
            step = step * 0.5
        iter_count += 1
    return current_t + step

def get_initial_ball_positions(num_balls, spacing=None):
    if spacing is None:
        spacing = settings.BALL_DIAMETER + settings.BALL_SPACING

    t_positions = []
    t = 0.0
    t_positions.append(t)

    for i in range(1, num_balls):
        next_t = find_t_at_distance(t, spacing, forward=True)
        t_positions.append(next_t)
        t = next_t

    return t_positions
