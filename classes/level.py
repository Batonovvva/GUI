# classes/level.py
import random
from typing import List, Dict, Any

from logic import spiral, settings
from classes.ball import Ball
from logic.settings import (
    PowerUp,
    POWERUP_DURATION,
    POWERUP_SLOW_FACTOR,
    BALL_DIAMETER,
    BALL_SPACING,
    SKULL_COLOR,
    BALL_COLORS,
)


class Level:
    def __init__(self, level_number: int):
        self.level_number = level_number
        self.config = settings.LEVELS.get(level_number, settings.LEVELS[1])

        # Параметры уровня
        self.base_spiral_speed = self.config["spiral_speed"]
        self.spiral_speed = self.base_spiral_speed
        self.time_remaining = self.config["time"]
        self.target_score = self.config["target_score"]
        self.skull_chance = self.config["skull_chance"]
        self.colors_count = self.config["colors_count"]
        self.chain = []

        self.generate_chain()
        self.active_powerups = []

    def generate_chain(self) -> None:
        """Генерирует начальную цепочку шариков, включая возможные бонусы и черепа."""
        self.chain.clear()
        initial_balls = self.config.get("initial_balls", 30)
        spacing = BALL_DIAMETER + BALL_SPACING
        t_values = spiral.get_initial_ball_positions(initial_balls, spacing=spacing)

        available_colors = BALL_COLORS[: self.colors_count]

        for t in t_values:
            roll = random.random()

            # 3% шанс — бонус замедления
            if roll < 0.03:
                color = (80, 200, 255)  # ярко-голубой
                ball_type = PowerUp.TYPE_SLOW
            elif roll < 0.05:
                color = (255, 100, 255)  # ярко-фиолетовый
                ball_type = PowerUp.TYPE_REVERSE
            elif roll < 0.07:
                color = (255, 200, 0)  # ярко-жёлтый
                ball_type = PowerUp.TYPE_FAST_SHOOT
            elif roll < 0.09:
                color = (255, 50, 50)  # ярко-красный
                ball_type = PowerUp.TYPE_EXPLOSION
            elif roll < 0.2:
                color = (25, 50, 50)  # ярко-красный
                ball_type = PowerUp.TYPE_BURST_SHOOT

            # 5–15% шанс — череп (зависит от уровня)
            elif roll < 0.03 + self.skull_chance:
                color = SKULL_COLOR
                ball_type = Ball.TYPE_SKULL
            else:
                color = random.choice(available_colors)
                ball_type = Ball.TYPE_NORMAL

            ball = Ball(color=color, t=t, ball_type=ball_type)
            self.chain.append(ball)



    def activate_powerup(self, powerup_type: str) -> None:
        """Активирует бонус (вызывается при попадании в бонусный шар)."""
        self.active_powerups.append({
            "type": powerup_type,
            "remaining": POWERUP_DURATION
        })
        print(f"[PowerUp] {powerup_type} активирован на {POWERUP_DURATION} сек")


    def update(self, dt: float) -> None:
        for p in self.active_powerups[:]:
            p["remaining"] -= dt
            if p["remaining"] <= 0:
                self.active_powerups.remove(p)

        # Определяем текущий модификатор скорости
        slow_factor = 1.0
        reverse_factor = 1.0  # 1 = вперед, -1 = назад

        for p in self.active_powerups:
            if p["type"] == PowerUp.TYPE_SLOW:
                slow_factor = min(slow_factor, POWERUP_SLOW_FACTOR)
            elif p["type"] == PowerUp.TYPE_REVERSE:
                reverse_factor = -1.0

        current_speed = self.spiral_speed * slow_factor * reverse_factor

        # Двигаем цепочку с учетом замедления
        for b in self.chain:
            b.update(dt, speed=current_speed)

        # Таймер уровня
        self.time_remaining = max(0.0, self.time_remaining - dt)

    def is_complete(self, score: int) -> bool:
        """Проверяет, пройден ли уровень."""
        return score >= self.target_score or self.time_remaining <= 0

    def spawn_skull(self) -> None:
        """Вставляет череп в начало цепочки (для продвинутых уровней)."""
        if random.random() < self.skull_chance:
            skull = Ball(color=SKULL_COLOR, t=0.0, ball_type=Ball.TYPE_SKULL)
            self.chain.insert(0, skull)
            # Пересчитываем t у всех шаров, чтобы не было наложения
            self._respace_chain()

    def _respace_chain(self) -> None:
        """Перераспределяет параметр t у всех шаров с учётом правильного расстояния."""
        if not self.chain:
            return
        spacing = BALL_DIAMETER + BALL_SPACING
        total_length = len(self.chain) * spacing
        start_t = self.chain[0].t
        for i, ball in enumerate(self.chain):
            ball.t = start_t + i * spacing / spiral.get_path_length_per_unit_t()