import random
from logic import spiral, settings
from classes.ball import Ball


class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.config = settings.LEVELS.get(level_number, settings.LEVELS[1])

        self.chain = []

        self.spiral_speed = self.config['spiral_speed']

        self.time_remaining = self.config['time']

        self.target_score = self.config['target_score']

        self.skull_chance = self.config['skull_chance']

        self.colors_count = self.config['colors_count']

        self.generate_chain()

        print(f"Level {level_number} started: time={self.time_remaining}, target={self.target_score}")

    def generate_chain(self):
        self.chain = []
        initial_balls = self.config.get('initial_balls', 20)
        spacing = settings.BALL_DIAMETER + settings.BALL_SPACING
        t_positions = spiral.get_initial_ball_positions(initial_balls, spacing=spacing)

        available_colors = settings.BALL_COLORS[: self.colors_count]

        for t in t_positions:
            is_skull = random.random() < self.skull_chance
            ball_type = Ball.TYPE_SKULL if is_skull else Ball.TYPE_NORMAL
            color = settings.SKULL_COLOR if is_skull else random.choice(available_colors)

            b = Ball(color=color, t=t, ball_type=ball_type)
            self.chain.append(b)


    def update(self, dt):
        for b in self.chain:
            b.update(dt, speed=self.spiral_speed)

        self.time_remaining -= dt
        if self.time_remaining < 0:
            self.time_remaining = 0

    def is_complete(self, score):
        return score >= self.target_score or self.time_remaining <= 0

    def spawn_skull(self):
        if random.random() < self.skull_chance:
            self.chain.insert(0, Ball(color=settings.SKULL_COLOR, t=0, ball_type='skull'))
