import math
import random

class PowerUp:
    TYPE_BURST_SHOOT = "burst_shoot"
    TYPE_SLOW = "slow"
    TYPE_FAST_SHOOT = "fast_shoot"
    TYPE_REVERSE = "reverse"
    TYPE_EXPLOSION = "explosion"

POWERUP_DURATION = 6.0       # секунд действия замедления
POWERUP_SLOW_FACTOR = 0.35

#ПАРАМЕТРЫ ЭКРАНА
WIDTH = 800
HEIGHT = 600
FPS = 60

#ЦВЕТА
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Цвета шариков
BALL_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
]

# Цвет черепа
SKULL_COLOR = (50, 50, 50)

#ПАРАМЕТРЫ ШАРИКОВ
BALL_RADIUS = 15
BALL_DIAMETER = BALL_RADIUS * 2
BALL_SPACING = 2  # Расстояние между шариками на спирали

#ПАРАМЕТРЫ СПИРАЛИ
SPIRAL_CENTER_X = WIDTH // 2
SPIRAL_CENTER_Y = HEIGHT // 2
SPIRAL_START_RADIUS = 250  # Начальный радиус спирали
SPIRAL_END_RADIUS = 30     # Конечный радиус (центр, проигрыш)
SPIRAL_TIGHTNESS = 1.5     # Коэффициент сжатия спирали
SPIRAL_SPEED = 1.5        # Базовая скорость движения шариков по спирали (пикселей за кадр)

#ИГРОВЫЕ ПРАВИЛА
MIN_MATCH = 3  # Минимальное количество шариков для удаления цепочки
POINTS_PER_BALL = 10  # Очки за удаление одного шарика
COMBO_MULTIPLIER = 1.5  # Множитель для комбо

#ПАРАМЕТРЫ ЛЯГУШКИ (ИГРОК)
FROG_X = WIDTH // 2
FROG_Y = HEIGHT // 2
FROG_RADIUS = 20  # Радиус лягушки
FROG_ROTATION_SPEED = 180  # Скорость поворота прицела (градусы за кадр)
SHOT_SPEED = 250  # Скорость полёта выстреленного шарика

#ПАРАМЕТРЫ ЧЕРЕПА
SKULL_SPAWN_CHANCE = 0.05  # Вероятность появления черепа (5%)
SKULL_EFFECT_RADIUS = 2  # Количество шариков вокруг черепа, которые удаляются

# ПАРАМЕТРЫ УРОВНЕЙ
LEVELS = {
    1: {
        'time': 60,  # Время уровня в секундах
        'target_score': 900,  # Целевые очки для прохождения
        'spiral_speed': 0.6,  # Скорость спирали
        'initial_balls': 50,  # Начальное количество шариков
        'skull_chance': 0.03,  # Вероятность черепа
        'colors_count': 4,  # Количество используемых цветов
    },
    2: {
        'time': 90,
        'target_score': 1000,
        'spiral_speed': 1,
        'initial_balls': 60,
        'skull_chance': 0.05,
        'colors_count': 5,
    },
    3: {
        'time': 120,
        'target_score': 1500,
        'spiral_speed': 1,
        'initial_balls': 60,
        'skull_chance': 0.07,
        'colors_count': 6,
    },
    4: {
        'time': 150,
        'target_score': 2500,
        'spiral_speed': 1,
        'initial_balls': 55,
        'skull_chance': 0.08,
        'colors_count': 6,
    },
    5: {
        'time': 180,
        'target_score': 4000,
        'spiral_speed': 1,
        'initial_balls': 40,
        'skull_chance': 0.1,
        'colors_count': 6,
    },
}

MAX_LEVEL = 5

#ПАРАМЕТРЫ UI
FONT_SIZE = 24
FONT_SIZE_LARGE = 36
UI_MARGIN = 10

# Цвета UI
UI_TEXT_COLOR = WHITE
UI_BACKGROUND_COLOR = (0, 0, 0, 128)  # Полупрозрачный черный
UI_TIMER_WARNING_COLOR = RED  # Цвет таймера при малом времени
UI_TIMER_WARNING_THRESHOLD = 10  # Секунды, когда таймер становится красным

#ПРОЧИЕ ПАРАМЕТРЫ
LIVES = 3  # Количество жизней игрока
COLLISION_DISTANCE = BALL_RADIUS + 5  # Расстояние для обнаружения столкновений

#МАТЕМАТИЧЕСКИЕ ФУНКЦИИ ДЛЯ СПИРАЛИ
def spiral_x(t):
    r = SPIRAL_START_RADIUS - t * SPIRAL_TIGHTNESS
    angle = t * 0.2
    return SPIRAL_CENTER_X + r * math.cos(angle)

def spiral_y(t):
    r = SPIRAL_START_RADIUS - t * SPIRAL_TIGHTNESS
    angle = t * 0.2
    return SPIRAL_CENTER_Y + r * math.sin(angle)

def get_spiral_position(t):
    return (spiral_x(t), spiral_y(t))

#Вспомогательная функция для позиций шариков
def get_initial_ball_positions(count: int):
    if count <= 0:
        return []

    start_t = 0.0
    end_t = (SPIRAL_START_RADIUS - SPIRAL_END_RADIUS) / SPIRAL_TIGHTNESS * 0.85

    step = end_t / (count + 1)
    t_values = [start_t + i * step for i in range(1, count + 1)]

    random.shuffle(t_values)

    return t_values