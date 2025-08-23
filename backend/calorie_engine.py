"""Deterministic calorie calculations."""
from dataclasses import dataclass


@dataclass
class Nutrition:
    protein: float
    carbs: float
    fat: float


def calories(nutrition: Nutrition) -> int:
    """Return caloric value based on macronutrients."""
    return int(nutrition.protein * 4 + nutrition.carbs * 4 + nutrition.fat * 9)
