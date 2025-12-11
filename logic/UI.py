from __future__ import annotations

import pygame
from logic.settings import *


pygame.font.init()
FONT = pygame.font.SysFont(None, FONT_SIZE)
FONT_LARGE = pygame.font.SysFont(None, FONT_SIZE_LARGE)


def draw_hud(screen, score, time_remaining, level_number, next_ball_color):
    score_text = FONT.render(f"Score: {score}", True, UI_TEXT_COLOR)
    screen.blit(score_text, (UI_MARGIN, UI_MARGIN))

    level_text = FONT.render(f"Level: {level_number}", True, UI_TEXT_COLOR)
    screen.blit(level_text, (UI_MARGIN, UI_MARGIN + 30))

    timer_color = UI_TEXT_COLOR
    if time_remaining <= UI_TIMER_WARNING_THRESHOLD:
        timer_color = UI_TIMER_WARNING_COLOR
    timer_text = FONT.render(f"Time: {int(time_remaining)}s", True, timer_color)
    screen.blit(timer_text, (UI_MARGIN, UI_MARGIN + 60))

    pygame.draw.circle(
        screen,
        next_ball_color,
        (WIDTH - FROG_RADIUS * 2, UI_MARGIN + FROG_RADIUS),
        FROG_RADIUS
    )
    pygame.draw.circle(
        screen,
        BLACK,
        (WIDTH - FROG_RADIUS * 2, UI_MARGIN + FROG_RADIUS),
        FROG_RADIUS,
        2
    )


def draw_pause_menu(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # полупрозрачный черный
    screen.blit(overlay, (0, 0))

    text = FONT_LARGE.render("PAUSED", True, WHITE)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)


def draw_level_complete(screen, score, target_score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    text1 = FONT_LARGE.render("LEVEL COMPLETE!", True, WHITE)
    rect1 = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text1, rect1)

    text2 = FONT.render(f"Score: {score} / {target_score}", True, WHITE)
    rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(text2, rect2)


def draw_game_over(screen, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    text1 = FONT_LARGE.render("GAME OVER", True, RED)
    rect1 = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text1, rect1)

    text2 = FONT.render(f"Final Score: {score}", True, WHITE)
    rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(text2, rect2)

def draw_menu(screen):
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(text, (
    WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + 100))

    font1 = pygame.font.SysFont(None, 84)
    text = font1.render("ZUMA", True, (255, 215, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 70))

def draw_victory(screen, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    title = FONT_LARGE.render("YOU WIN!", True, (255, 215, 0))  # золотой
    trect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(title, trect)

    text = FONT.render(f"Final Score: {score}", True, WHITE)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
    screen.blit(text, rect)

    hint = FONT.render("Press Enter to play again or Esc to exit", True, WHITE)
    hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(hint, hint_rect)
def draw_slow_effect(screen, intensity=120):
    """
    Полупрозрачный синий/голубой оверлей для ощущения 'замедления'.
    intensity: 0..255 alpha слоя (по умолчанию 120).
    Также рисуем лёгкую виньетку (чёрная градиентная рамка).
    """
    # базовый голубой тон
    w, h = screen.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)

    # мягкий голубой прозрачный слой
    a = max(0, min(255, int(intensity)))
    overlay.fill((60, 130, 220, a // 2))

    # простой виньеточный градиент по краям (не слишком тяжёлый)
    # рисуем несколько полупрозрачных концентрических прямоугольников
    steps = 6
    max_alpha = int(a * 0.6)
    for i in range(steps):
        frac = (i + 1) / steps
        rect = pygame.Rect(int(w * (-0.05 * frac)), int(h * (-0.05 * frac)),
                           int(w * (1 + 0.1 * frac)), int(h * (1 + 0.1 * frac)))
        alpha = int(max_alpha * (frac ** 2))
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((0, 10, 20, alpha))
        screen.blit(s, (rect.x, rect.y))

    # немного размытия симуляцией: копируем и смещяем для мягкости
    # (быстрая имитация размытия — не реальные фильтры)
    for dx, dy, mul in ((-2, -1, 0.06), (2, 1, 0.04), (0, 0, 0.9)):
        tmp = overlay.copy()
        tmp.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        screen.blit(tmp, (dx, dy), special_flags=pygame.BLEND_RGBA_ADD if mul > 0.5 else 0)

    # финальный общий оверлей
    screen.blit(overlay, (0, 0))


def draw_slow_particles(screen, amount=25, seed: int | None = None):
    w, h = screen.get_size()
    now = pygame.time.get_ticks() / 1000.0

    import random
    rnd = random.Random(seed if seed is not None else int(now * 1000))

    for i in range(amount):
        fx = ( (i * 37) % (w + 1) ) / max(1, w)
        fy = ( (i * 73) % (h + 1) ) / max(1, h)

        tx = fx * w + math.sin(now * (0.5 + (i % 7) * 0.13) + i) * (10 + (i % 5) * 4)
        ty = fy * h + math.cos(now * (0.4 + (i % 5) * 0.11) + i * 0.7) * (8 + (i % 3) * 3) + now * 6.0 * ((i % 2) * 0.2 + 0.5)

        base_alpha = 80 + (i % 5) * 12
        alpha = max(30, min(220, int(base_alpha)))
        radius = 1 + (i % 4)

        surf = pygame.Surface((radius * 4 + 2, radius * 4 + 2), pygame.SRCALPHA)
        # легкий голубой/белый оттенок
        col = (200, 220, 255, alpha)
        pygame.draw.circle(surf, col, (surf.get_width() // 2, surf.get_height() // 2), radius)
        # альфа в зависимости от вертикальной позиции (необязательно)
        vfade = 1.0 - (abs((ty / h) - 0.5) * 1.2)
        if vfade < 0.2:
            vfade = 0.2
        # применяем вертикальную модуляцию
        surf.fill((255, 255, 255, int(alpha * vfade)), special_flags=pygame.BLEND_RGBA_MULT)

        # blit на экран (округляем позицию)
        screen.blit(surf, (int(tx) - surf.get_width() // 2, int(ty) - surf.get_height() // 2))
