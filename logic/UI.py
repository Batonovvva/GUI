import pygame
import settings


pygame.font.init()
FONT = pygame.font.SysFont(None, settings.FONT_SIZE)
FONT_LARGE = pygame.font.SysFont(None, settings.FONT_SIZE_LARGE)


def draw_hud(screen, score, time_remaining, level_number, next_ball_color):
    score_text = FONT.render(f"Score: {score}", True, settings.UI_TEXT_COLOR)
    screen.blit(score_text, (settings.UI_MARGIN, settings.UI_MARGIN))

    level_text = FONT.render(f"Level: {level_number}", True, settings.UI_TEXT_COLOR)
    screen.blit(level_text, (settings.UI_MARGIN, settings.UI_MARGIN + 30))

    timer_color = settings.UI_TEXT_COLOR
    if time_remaining <= settings.UI_TIMER_WARNING_THRESHOLD:
        timer_color = settings.UI_TIMER_WARNING_COLOR
    timer_text = FONT.render(f"Time: {int(time_remaining)}s", True, timer_color)
    screen.blit(timer_text, (settings.UI_MARGIN, settings.UI_MARGIN + 60))

    pygame.draw.circle(
        screen,
        next_ball_color,
        (settings.WIDTH - settings.FROG_RADIUS * 2, settings.UI_MARGIN + settings.FROG_RADIUS),
        settings.FROG_RADIUS
    )
    pygame.draw.circle(
        screen,
        settings.BLACK,
        (settings.WIDTH - settings.FROG_RADIUS * 2, settings.UI_MARGIN + settings.FROG_RADIUS),
        settings.FROG_RADIUS,
        2
    )


def draw_pause_menu(screen):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # полупрозрачный черный
    screen.blit(overlay, (0, 0))

    text = FONT_LARGE.render("PAUSED", True, settings.WHITE)
    rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
    screen.blit(text, rect)


def draw_level_complete(screen, score, target_score):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    text1 = FONT_LARGE.render("LEVEL COMPLETE!", True, settings.WHITE)
    rect1 = text1.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 40))
    screen.blit(text1, rect1)

    text2 = FONT.render(f"Score: {score} / {target_score}", True, settings.WHITE)
    rect2 = text2.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 20))
    screen.blit(text2, rect2)


def draw_game_over(screen, score):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    text1 = FONT_LARGE.render("GAME OVER", True, settings.RED)
    rect1 = text1.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 40))
    screen.blit(text1, rect1)

    text2 = FONT.render(f"Final Score: {score}", True, settings.WHITE)
    rect2 = text2.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 20))
    screen.blit(text2, rect2)

def draw_menu(screen):
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press ENTER to Start", True, (255, 255, 255))
    screen.blit(text, (
    settings.WIDTH // 2 - text.get_width() // 2, settings.HEIGHT // 2 - text.get_height() // 2 + 100))

    font1 = pygame.font.SysFont(None, 84)
    text = font1.render("ZUMA", True, (255, 215, 0))
    screen.blit(text, (settings.WIDTH // 2 - text.get_width() // 2, settings.HEIGHT // 2 - text.get_height() // 2 - 70))

def draw_victory(screen, score):
    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    title = FONT_LARGE.render("YOU WIN!", True, (255, 215, 0))  # золотой
    trect = title.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 40))
    screen.blit(title, trect)

    text = FONT.render(f"Final Score: {score}", True, settings.WHITE)
    rect = text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 10))
    screen.blit(text, rect)

    hint = FONT.render("Press Enter to play again or Esc to exit", True, settings.WHITE)
    hint_rect = hint.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 60))
    screen.blit(hint, hint_rect)

