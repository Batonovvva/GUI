from __future__ import annotations

from settings import *
from classes.ball import Ball
import spiral
import settings


CHAIN_GAP_T = (BALL_DIAMETER + BALL_SPACING) / SPIRAL_TIGHTNESS
SPIRAL_END_T = (SPIRAL_START_RADIUS - SPIRAL_END_RADIUS) / SPIRAL_TIGHTNESS

def respace_chain(chain, spacing=None, start_t=None):
    if spacing is None:
        spacing = settings.BALL_DIAMETER + settings.BALL_SPACING

    if not chain:
        return

    if start_t is None:
        try:
            start_t = chain[0].t
        except Exception:
            start_t = 0.0

    t_positions = [start_t]
    for i in range(1, len(chain)):
        next_t = spiral.find_t_at_distance(t_positions[-1], spacing, forward=True)
        t_positions.append(next_t)

    for b, t in zip(chain, t_positions):
        b.t = t
        if hasattr(b, "calculate_position"):
            b.pos = b.calculate_position()
        else:
            b.pos = spiral.get_position(t)


def add_wave(chain: list[Ball], count: int, skull_freq: float = SKULL_SPAWN_CHANCE, colors: list = BALL_COLORS):
    start_t = chain[0].t - CHAIN_GAP_T if chain else 0.0
    for i in range(count):
        color = random.choice(colors)
        is_skull = random.random() < skull_freq
        ball_type = Ball.TYPE_SKULL if is_skull else Ball.TYPE_NORMAL
        t = start_t - i * CHAIN_GAP_T
        ball = Ball(color=color, ball_type=ball_type, t=t)
        chain.insert(0, ball)


def update_chain(chain: list[Ball], dt: float, speed: float) -> str | None:
    for ball in chain:
        ball.update(dt, speed=speed)
    if chain and chain[-1].t >= SPIRAL_END_T:
        return "game_over"
    return None


def draw_chain(screen, chain: list[Ball]):
    for ball in chain:
        ball.draw(screen)


def insert_ball(chain: list[Ball], ball: Ball, index: int) -> int:
    if 0 < index < len(chain):
        ball.t = (chain[index - 1].t + chain[index].t) / 2
    elif index > 0:
        ball.t = chain[index - 1].t + CHAIN_GAP_T
    else:
        ball.t = chain[0].t - CHAIN_GAP_T if chain else 0.0

    chain.insert(index, ball)
    ball.is_projectile = False
    return index


def find_match(chain: list[Ball], index: int) -> list[int]:
    if not (0 <= index < len(chain)):
        return []

    color = chain[index].color
    left = right = index
    while left > 0 and chain[left - 1].color == color:
        left -= 1
    while right < len(chain) - 1 and chain[right + 1].color == color:
        right += 1

    if right - left + 1 >= MIN_MATCH:
        return list(range(left, right + 1))
    return []


def remove_chain(chain: list[Ball], indices: list[int]) -> int:
    if not indices:
        return 0
    for i in sorted(indices, reverse=True):
        del chain[i]
    return len(indices) * POINTS_PER_BALL


def handle_skull(chain: list[Ball], index: int) -> tuple[int, list[int]]:
    radius = SKULL_EFFECT_RADIUS
    start = max(0, index - radius)
    end = min(len(chain) - 1, index + radius)
    indices = list(range(start, end + 1))
    score = remove_chain(chain, indices)
    return -score // 2, indices


def rollback_chain(chain: list[Ball], removed_count: int):
    if removed_count == 0:
        return
    shift = CHAIN_GAP_T * removed_count * 0.8
    for ball in chain:
        ball.t -= shift


def handle_insertion(chain: list[Ball], projectile: Ball) -> tuple[int, list[int]]:
    pos = projectile.get_pos()
    insert_idx = None
    for i, b in enumerate(chain):
        if b.get_pos().distance_to(pos) < COLLISION_DISTANCE:
            insert_idx = i
            break
    if insert_idx is None:
        return 0, []

    insert_idx = insert_ball(chain, projectile, insert_idx)
    ball = chain[insert_idx]

    score = 0
    removed = []

    if ball.type == Ball.TYPE_SKULL:
        score, removed = handle_skull(chain, insert_idx)
    else:
        match = find_match(chain, insert_idx)
        if match:
            score = remove_chain(chain, match)
            removed = match
            rollback_chain(chain, len(match))

    return score, removed