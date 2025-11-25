import settings
import math

def check_collision(flying_ball, chain):
    for i, ball in enumerate(chain):
        dx = flying_ball.pos[0] - ball.pos[0]
        dy = flying_ball.pos[1] - ball.pos[1]
        distance = math.hypot(dx, dy)

        if distance <= flying_ball.radius + ball.radius:
            return i

    return None
