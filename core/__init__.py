"""
核心游戏逻辑与规则包
"""

from importlib import util
from pathlib import Path

_core_path = Path(__file__).resolve().parent.parent / "core.py"
_spec = util.spec_from_file_location("_legacy_core", _core_path)
_legacy_core = util.module_from_spec(_spec)
_spec.loader.exec_module(_legacy_core)

Card = _legacy_core.Card
Deck = _legacy_core.Deck
HandState = _legacy_core.HandState
Player = _legacy_core.Player
Table = _legacy_core.Table

__all__ = [
    "Card",
    "Deck",
    "HandState",
    "Player",
    "Table",
]
