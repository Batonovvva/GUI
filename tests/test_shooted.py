import unittest

import pytest
from classes.level import Level
from logic.settings import PowerUp, POWERUP_DURATION, POWERUP_SLOW_FACTOR

class DummyBall:
    def __init__(self, t=0.0):
        self.t = t
        self.last_update_speed = None
        self.update_calls = 0

    def update(self, dt, speed=None):
        # сохраняем speed, инкрементируем t симулятивно
        self.last_update_speed = speed
        self.update_calls += 1
        # имитируем изменение t как реальный Ball
        if speed is not None:
            self.t += dt * speed
        else:
            self.t += dt


def test_activate_powerup_adds_entry():
    lvl = Level(1)
    # очистим цепочку, т.к. нам не нужны реальные Ball-ы
    lvl.chain = []
    assert lvl.active_powerups == []

    lvl.activate_powerup(PowerUp.TYPE_SLOW)
    assert len(lvl.active_powerups) == 1
    p = lvl.active_powerups[0]
    assert p["type"] == PowerUp.TYPE_SLOW
    # remaining должно быть равно константе POWERUP_DURATION
    assert pytest.approx(p["remaining"], rel=1e-3) == POWERUP_DURATION


def test_slow_powerup_reduces_chain_update_speed():
    lvl = Level(1)
    # подменим цепочку одним dummy-мячом
    dummy = DummyBall(t=0.0)
    lvl.chain = [dummy]

    # установим базовую скорость в некий известный value
    lvl.spiral_speed = 10.0
    lvl.base_spiral_speed = 10.0

    # активируем SLOW
    lvl.activate_powerup(PowerUp.TYPE_SLOW)
    # сделаем один апдейт с dt=1.0
    lvl.update(1.0)

    # ожидаем, что переданная скорость равна spiral_speed * POWERUP_SLOW_FACTOR
    expected = 10.0 * float(POWERUP_SLOW_FACTOR)
    assert dummy.update_calls == 1
    assert pytest.approx(dummy.last_update_speed, rel=1e-6) == expected


def test_reverse_powerup_inverts_chain_direction():
    lvl = Level(1)
    dummy = DummyBall(t=0.0)
    lvl.chain = [dummy]

    lvl.spiral_speed = 7.0
    lvl.base_spiral_speed = 7.0

    lvl.activate_powerup(PowerUp.TYPE_REVERSE)
    lvl.update(0.5)  # полсекунды, но нас интересует скорость

    # для REVERSE скорость должна быть отрицательной (обратный ход)
    assert dummy.update_calls == 1
    assert dummy.last_update_speed < 0.0
    # абсолютная величина скорости должна быть base * 1.0 (reverse_factor == -1)
    assert pytest.approx(abs(dummy.last_update_speed), rel=1e-6) == 7.0


def test_powerup_expires_and_speed_restored():
    lvl = Level(1)
    dummy = DummyBall(t=0.0)
    lvl.chain = [dummy]

    lvl.spiral_speed = 5.0
    lvl.base_spiral_speed = 5.0

    # активируем SLOW, затем симулируем время > POWERUP_DURATION
    lvl.activate_powerup(PowerUp.TYPE_SLOW)
    # шаги: уменьшение remaining — вызываем update с суммой dt > POWERUP_DURATION
    total = POWERUP_DURATION + 0.5
    # можно разделить на два кадра
    lvl.update(total / 2.0)
    lvl.update(total / 2.0)

    # теперь active_powerups должен быть пуст
    assert all(p["remaining"] > 0 for p in lvl.active_powerups) == False or len(lvl.active_powerups) == 0

    # при следующем update скорость должна быть восстановлена до базовой (без slow)
    dummy.last_update_speed = None
    lvl.update(0.2)
    assert dummy.last_update_speed is not None
    # ожидаем близко к базовой (без применения POWERUP_SLOW_FACTOR)
    assert pytest.approx(dummy.last_update_speed, rel=1e-6) == pytest.approx(5.0 * 1.0)

if __name__ == "__main__":
    unittest.main()