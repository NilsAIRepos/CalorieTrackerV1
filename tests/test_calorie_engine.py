"""Unit tests for the calorie engine."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.calorie_engine import Nutrition, calories


def test_calorie_computation() -> None:
    """Calorie calculation follows macronutrient formula."""
    n = Nutrition(protein=10, carbs=20, fat=5)
    assert calories(n) == 10 * 4 + 20 * 4 + 5 * 9
