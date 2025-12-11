import pytest
from classes.game import Game
from classes.ball import Ball
from classes.frog import Frog
from types import SimpleNamespace

def test_game_start_level_creates_level_and_sets_state():
    g = Game()
    g.start_level(1)
    assert g.state == "playing"
    assert g.level is not None
    assert isinstance(g.frog, Frog)
    assert g.score == 0

def test_game_picks_up_powerup_on_collision(monkeypatch):
    g = Game()
    g.start_level(1)
    # put a powerup ball at index 0
    pu_ball = Ball(color=(1,2,3), t=0.0, ball_type="slow")
    # ensure level.chain has at least one element; insert at 0
    g.level.chain.insert(0, pu_ball)
    # create a dummy flying ball
    class DummyBall:
        def __init__(self):
            self.pos = [0.0, 0.0]
            self.dx = 0.0
            self.dy = 0.0
            self.speed = 1.0
            self.color = (10,10,10)
            self.type = "normal"
        def update(self, dt):
            pass
        def is_offscreen(self):
            return False

    db = DummyBall()
    g.flying_balls.append(db)
    # monkeypatch check_collision to always return index 0
    monkeypatch.setattr("logic.collision.check_collision", lambda ball, chain: 0)
    # run update once: should activate powerup and remove flying ball and remove chain element
    before_score = g.score
    before_chain_len = len(g.level.chain)
    g.update(0.016)
    assert g.score >= before_score + 150
    assert db not in g.flying_balls
    assert len(g.level.chain) == before_chain_len - 1
    # ensure level.active_powerups contains slow
    assert any(p["type"] == "slow" for p in g.level.active_powerups)
