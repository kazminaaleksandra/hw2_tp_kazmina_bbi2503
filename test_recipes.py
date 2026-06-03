import pytest
from recipe import Ingredient  

class TestIngredient:
    def test_formation(self):
        ingredient = Ingredient("Мука", 500.0, "г")
        assert ingredient.name == "Мука"
        assert ingredient.quantity == 500.0
        assert ingredient.unit == "г"

    def test_str_representation(self):
        ingredient = Ingredient("Нут", 250.0, "г")
        assert str(ingredient) == "Нут: 250.0 г"

    def test_eq_quantity_ignored(self):
        ingredient1 = Ingredient("Сахар", 10.0, "г")
        ingredient2 = Ingredient("Сахар", 20.0, "г")
        assert ingredient1 == ingredient2

    def test_eq_different_name(self):
        ingredient1 = Ingredient("Мука", 500.0, "г")
        ingredient2 = Ingredient("Сахар", 500.0, "г")
        assert ingredient1 != ingredient2

    def test_eq_different_unit(self):
        ingredient1 = Ingredient("Матча", 50.0, "г")
        ingredient2 = Ingredient("Матча", 50.0, "кг")
        assert ingredient1 != ingredient2
