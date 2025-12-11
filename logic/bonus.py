# # logic/bonus.py
# from dataclasses import dataclass
# from enum import Enum, auto
#
# class BonusType(Enum):
#     SLOW = auto()        # замедление спирали (multiplier < 1)
#     REVERSE = auto()     # обратный ход (invert direction)
#     RAPID_FIRE = auto()       # увеличение скорострельности (cooldown multiplier < 1)
#     EXPLOSION = auto()   # следующий выстрел(ы) взрываются, удаляют соседей (radius)
#     BURST = auto()       # стрельба очередью (burst_count > 1)
#     EXTRA_LIFE = auto()  # +1 жизнь
#     SCORE = auto()       # мгновенные очки
#
# @dataclass
# class Bonus:
#     type: BonusType
#     duration: float = 0.0   # seconds; 0 => instant
#     value: float = 0.0      # generic value (factor/points/radius/count)
#     remaining: float = 0.0
#     applied: bool = False
#
#     def start(self):
#         self.remaining = self.duration
#         self.applied = False
#
#     def tick(self, dt: float):
#         if self.duration > 0:
#             self.remaining = max(0.0, self.remaining - dt)
#
#     def is_expired(self) -> bool:
#         return self.duration > 0 and self.remaining <= 0.0
