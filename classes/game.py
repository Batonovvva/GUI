import sys
import pygame
from classes.frog import Frog
from classes.level import Level
from classes.ball import Ball
try:
    from flying import FlyingBall
except Exception:
    FlyingBall = None
from logic.chain import find_match, remove_chain, handle_skull, respace_chain
from logic.collision import check_collision
from logic.UI import draw_hud, draw_pause_menu, draw_level_complete, draw_game_over, draw_menu, draw_victory
from logic.settings import *  # импортируем константы: LIVES, MAX_LEVEL, POINTS_PER_BALL, COMBO_MULTIPLIER, BALL_DIAMETER, BALL_SPACING, BALL_RADIUS, WIDTH, HEIGHT, BLACK

# безопасный helper для значений из settings (если что-то не определено)
def _get_setting(name: str, default):
    return globals().get(name, default)


class Game:
    def __init__(self, screen=None):
        self.screen = screen

        self.state = "menu"

        self.level_number = 1
        self.level = None
        self.frog = Frog()
        # либо берем LIVES, либо default 3
        self.score = 0
        self.lives = _get_setting("LIVES", 3)

        self.flying_balls = []

        self._debug = False
        self.max_levels = _get_setting("MAX_LEVEL", 1)

    def start_level(self, level_number=None):
        if level_number is not None:
            self.level_number = level_number

        if self.level_number > self.max_levels:
            self.state = "victory"
            return
        self.level = Level(self.level_number)
        self.frog = Frog()
        self.score = 0
        self.flying_balls.clear()
        self.state = "playing"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEMOTION:
                try:
                    self.frog.aim_at(event.pos)
                except Exception:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                new_ball = self.frog.shoot(aim_pos=mouse_pos)
                if new_ball:
                    self.flying_balls.extend(new_ball)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"
                    elif self.state == "victory":
                        sys.exit()
                if self.state == "playing":
                    if event.key == pygame.K_LEFT:
                        self.frog.rotate(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.frog.rotate(1)
                    elif event.key == pygame.K_SPACE:
                        new_ball = self.frog.shoot()
                        if new_ball:
                            self.flying_balls.extend(new_ball)
                    elif event.key == pygame.K_p:
                        self.state = "paused"
                else:
                    if event.key == pygame.K_RETURN:
                        if self.state == "menu":
                            self.start_level(1)
                        elif self.state == "level_complete":
                            self.level_number += 1
                            self.start_level(self.level_number)
                        elif self.state == "game_over":
                            self.level_number = 1
                            self.start_level(self.level_number)
                        elif self.state == "victory":
                            self.level_number = 1
                            self.start_level(self.level_number)

    def update(self, dt):
        if self.state != "playing":
            return

        if self.level:
            self.level.update(dt)

        if hasattr(self.frog, "update"):
            try:
                self.frog.update(dt)
            except Exception:
                pass

        for ball in self.flying_balls[:]:
            try:
                ball.update(dt)
            except AttributeError:
                if hasattr(ball, "dx") and hasattr(ball, "dy") and hasattr(ball, "speed") and hasattr(ball, "pos"):
                    ball.pos[0] += ball.dx * ball.speed * dt
                    ball.pos[1] += ball.dy * ball.speed * dt

            # Проверяем столкновение с цепочкой
            if self.level and getattr(self.level, "chain", None):
                idx = check_collision(ball, self.level.chain)
            else:
                idx = None

            if idx is not None:
                # ===== если попали в ЧЕРЕП в цепочке — мгновенный Game Over =====
                target_stationary = self.level.chain[idx]
                if getattr(target_stationary, "type", Ball.TYPE_NORMAL) == Ball.TYPE_SKULL:
                    self.state = "game_over"
                    return

                target_stationary = self.level.chain[idx]
                ball_type = getattr(target_stationary, "type", Ball.TYPE_NORMAL)

                # Бонус замедления
                if ball_type == PowerUp.TYPE_SLOW:
                    self.level.activate_powerup(PowerUp.TYPE_SLOW)
                    self.level.chain.pop(idx)  # удаляем бонусный шар
                    self.score += 150           # очки за бонус
                    if ball in self.flying_balls:
                        self.flying_balls.remove(ball)
                    continue

                # reverse
                elif ball_type == PowerUp.TYPE_REVERSE:
                    self.level.activate_powerup(PowerUp.TYPE_REVERSE)
                    self.level.chain.pop(idx)
                    self.score += 150
                    if ball in self.flying_balls:
                        self.flying_balls.remove(ball)
                    continue

                # fast_shoot
                elif ball_type == PowerUp.TYPE_FAST_SHOOT:
                    self.level.activate_powerup(PowerUp.TYPE_FAST_SHOOT)
                    self.frog.shoot_speed_multiplier = 1.5  # например, +50% скорость
                    self.level.chain.pop(idx)
                    self.score += 150
                    if ball in self.flying_balls:
                        self.flying_balls.remove(ball)
                    continue

                # burst_shoot
                elif ball_type == PowerUp.TYPE_BURST_SHOOT:
                    self.frog.burst_shoot_count = 3
                    self.frog.burst_timer = POWERUP_DURATION
                    self.level.chain.pop(idx)
                    self.score += 150
                    if ball in self.flying_balls:
                        self.flying_balls.remove(ball)
                    continue

                # Проверяем таймер бонуса Burst Shoot
                if hasattr(self.frog, "burst_timer") and self.frog.burst_timer > 0:
                    self.frog.burst_timer -= dt
                    if self.frog.burst_timer <= 0:
                        self.frog.burst_shoot_count = 1


                if ball_type == PowerUp.TYPE_EXPLOSION:
                    self.level.activate_powerup(PowerUp.TYPE_EXPLOSION)

                    idx_hit = idx
                    explosion_radius = 3
                    start_idx = max(0, idx_hit - explosion_radius)
                    end_idx = min(len(self.level.chain) - 1, idx_hit + explosion_radius)
                    indices_to_remove = list(range(start_idx, end_idx + 1))

                    removed_count = remove_chain(self.level.chain, indices_to_remove)
                    self.score += removed_count * _get_setting("POINTS_PER_BALL", 10)

                    if ball in self.flying_balls:
                        self.flying_balls.remove(ball)

                    self.level.chain.pop(idx_hit)
                    continue

                # ===== если летящий шар сам — череп (bomb) =====
                if getattr(ball, "type", Ball.TYPE_NORMAL) == Ball.TYPE_SKULL:
                    removed = handle_skull(self.level.chain, idx)
                    self.score += len(removed) * _get_setting("POINTS_PER_BALL", 10)
                else:
                    # Вставляем новый stationary Ball на место столкновения
                    neighbor_t = self.level.chain[idx].t if idx < len(self.level.chain) else (
                        self.level.chain[-1].t if self.level.chain else 0.0
                    )
                    new_t = neighbor_t + 0.01
                    new_ball = Ball(ball.color, new_t, Ball.TYPE_NORMAL)
                    self.level.chain.insert(idx, new_ball)

                    # Перераспределяем t по цепочке
                    spacing = _get_setting("BALL_DIAMETER", 32) + _get_setting("BALL_SPACING", 2)
                    outer_t = self.level.chain[0].t if self.level.chain else 0.0
                    respace_chain(self.level.chain, spacing=spacing, start_t=outer_t)

                    match_indices = find_match(self.level.chain, idx)
                    if match_indices:
                        removed_count = remove_chain(self.level.chain, match_indices)
                        self.score += int(
                            removed_count *
                            _get_setting("POINTS_PER_BALL", 10) *
                            _get_setting("COMBO_MULTIPLIER", 1)
                        )

                # Удаляем летящий шарик (один раз)
                if ball in self.flying_balls:
                    try:
                        self.flying_balls.remove(ball)
                    except ValueError:
                        pass
                continue

            # Если шарик улетел за экран — удаляем
            try:
                if hasattr(ball, "is_offscreen") and ball.is_offscreen():
                    if ball in self.flying_balls:
                        self.flying_balls.remove(ball)
                    continue
            except Exception:
                if hasattr(ball, "pos"):
                    bx, by = ball.pos[0], ball.pos[1]
                    if bx < -_get_setting("BALL_RADIUS", 16) or bx > _get_setting("WIDTH", 800) + _get_setting("BALL_RADIUS", 16) \
                       or by < -_get_setting("BALL_RADIUS", 16) or by > _get_setting("HEIGHT", 600) + _get_setting("BALL_RADIUS", 16):
                        if ball in self.flying_balls:
                            self.flying_balls.remove(ball)
                        continue

        # Проверка: достигла ли цепочка центра (и есть ли череп среди достигших)
        if self.level and getattr(self.level, "chain", None):
            for stationary in list(self.level.chain):
                try:
                    if stationary.is_at_end():
                        if getattr(stationary, "type", Ball.TYPE_NORMAL) == Ball.TYPE_SKULL:
                            self.state = "game_over"
                            return
                        # Обычный шарик — уменьшаем жизни или game over
                        self.lives -= 1
                        if self.lives <= 0:
                            self.state = "game_over"
                            return
                except Exception:
                    pass

        # Проверка завершения уровня (таймер/очки)
        if self.level and self.level.is_complete(self.score):
            if self.score >= getattr(self.level, "target_score", 0):
                self.state = "level_complete"
            else:
                self.state = "game_over"

    def draw(self, screen):
        screen.fill(_get_setting("BLACK", (0, 0, 0)))

        if self.state == "menu":
            draw_menu(screen)

        elif self.state in ("playing", "paused"):
            if self.level:
                for b in self.level.chain:
                    try:
                        b.draw(screen)
                    except Exception:
                        pass

            for fb in self.flying_balls:
                try:
                    fb.draw(screen)
                except Exception:
                    if hasattr(fb, "pos") and hasattr(fb, "color") and hasattr(fb, "radius"):
                        pygame.draw.circle(screen, fb.color, (int(fb.pos[0]), int(fb.pos[1])), int(fb.radius))

            try:
                self.frog.draw(screen)
            except Exception:
                pass

            next_color = getattr(self.frog, "next_ball_color", getattr(self.frog, "current_ball_color", (255, 255, 255)))
            draw_hud(screen, self.score, getattr(self.level, "time_remaining", 0), self.level_number, next_color)

            if self.state == "paused":
                draw_pause_menu(screen)

        elif self.state == "level_complete":
            draw_level_complete(screen, self.score, getattr(self.level, "target_score", 0))

        elif self.state == "game_over":
            draw_game_over(screen, self.score)

        elif self.state == "victory":
            draw_victory(screen, self.score)

    def toggle_pause(self):
        if self.state == "playing":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "playing"