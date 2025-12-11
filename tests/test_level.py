import random
import pytest
from classes.level import Level
from classes.ball import Ball
from logic import settings
from logic import spiral

def test_generate_chain_length():
    lvl = Level(1)
    expected = lvl.config.get("initial_balls", settings.LEVELS[1]['initial_balls'])
    assert isinstance(lvl.chain, list)
    assert len(lvl.chain) == expected

def test_update_moves_chain_and_decreases_timer():
    lvl = Level(1)
    # snapshot first ball t
    if not lvl.chain:
        pytest.skip("no balls generated")
    t_before = lvl.chain[0].t
    time_before = lvl.time_remaining
    lvl.update(1.0)
    # timer decreased
    assert lvl.time_remaining == pytest.approx(max(0.0, time_before - 1.0))
    # first ball t moved (speed might be zero for weird configs but usually >0)
    assert lvl.chain[0].t != pytest.approx(t_before)

def test_activate_powerup_adds_active_powerup():
    lvl = Level(1)
    lvl.activate_powerup("slow")
    assert any(p["type"] == "slow" for p in lvl.active_powerups)
    assert all("remaining" in p for p in lvl.active_powerups)
