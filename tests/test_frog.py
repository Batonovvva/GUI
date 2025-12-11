import unittest

import pygame
import types
import random
from classes.frog import Frog
from classes.flying_ball import FlyingBall
from logic import settings

def test_flying_ball_moves():
    fb = FlyingBall(100, 100, 1.0, 0.0, color=(10,20,30), speed=100.0, radius=5)
    x0, y0 = fb.pos[0], fb.pos[1]
    fb.update(0.1)
    assert fb.pos[0] > x0

def test_frog_shoot_changes_colors_and_creates_ball(monkeypatch):
    # ensure pygame time returns something big so can_shoot passes
    monkeypatch.setattr("pygame.time.get_ticks", lambda: 100000)
    frog = Frog()
    frog._last_shot_time = 0.0
    # set deterministic colors
    frog.current_ball_color = (11,22,33)
    frog.next_ball_color = (44,55,66)
    # shoot towards center (use aim_pos to get direction)
    res = frog.shoot(aim_pos=(0, 0))
    # shoot returns a FlyingBall or list; normalize:
    if isinstance(res, list):
        fb = res[0]
    else:
        fb = res
    assert fb.color == (11,22,33)
    # after shooting current becomes previous next
    assert frog.current_ball_color == (44,55,66)

if __name__ == "__main__":
    unittest.main()