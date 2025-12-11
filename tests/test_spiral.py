import math
import unittest

from logic import spiral
from logic import settings

def test_get_position_returns_tuple():
    p = spiral.get_position(0.0)
    assert isinstance(p, tuple) and len(p) == 2

def test_radius_decreases_with_t():
    r0 = spiral.get_radius(0.0)
    r1 = spiral.get_radius(10.0)
    assert r1 <= r0

def test_distance_between_t_positive():
    d = spiral.distance_between_t(0.0, 5.0)
    assert d >= 0.0

def test_find_t_at_distance_monotonic():
    t0 = 0.0
    spacing = settings.BALL_DIAMETER + settings.BALL_SPACING
    t1 = spiral.find_t_at_distance(t0, spacing, forward=True)
    assert isinstance(t1, float)
    assert t1 != t0

if __name__ == "__main__":
    unittest.main()
