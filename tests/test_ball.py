import unittest

import pytest
from classes.ball import Ball
from logic import spiral, settings

def test_ball_calculate_position_matches_spiral():
    b = Ball(color=(10,20,30), t=0.0, ball_type=Ball.TYPE_NORMAL)
    assert b.pos == spiral.get_position(0.0)
    assert b.radius == settings.BALL_RADIUS

def test_ball_update_advances_t_and_pos():
    b = Ball(color=(1,2,3), t=0.0)
    old_t = b.t
    b.update(0.5, speed=2.0)
    assert b.t > old_t
    assert b.pos == spiral.get_position(b.t)

def test_ball_distance_to_point_and_is_at_end():
    b = Ball(color=(1,2,3), t=0.0)
    # distance to itself is zero
    assert pytest.approx(b.distance_to(b), rel=1e-6) == 0.0
    # is_at_end returns boolean
    assert isinstance(b.is_at_end(), bool)

if __name__ == "__main__":
    unittest.main()