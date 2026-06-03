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

class TestRecipe:
    def test_formation(self):
        ingredients = [Ingredient("Мука", 500.0,"г")]
        recipe = Recipe("Блинчики", ingredients)
        assert recipe.title == "Блинчики"
        assert recipe.ingredients == ingredients

    def test_add_ingredient_new_one(self):
        recipe = Recipe("Битые огурцы", [])
        ingredient = Ingredient("Огурец", 6.0, "шт")
        recipe.add_ingredient(ingredient)
        assert ingredient in recipe.ingredients
        assert len(recipe.ingredients) == 1

    def test_add_ingredient_accumulates(self):
        recipe = Recipe("Лазанья", [Ingredient("Фарш", 700.0, "г")])
        new_ingredient = Ingredient("Фарш", 715.0, "г")
        recipe.add_ingredient(new_ingredient)
        assert len(recipe.ingredients) == 1
        added_ingredient = recipe.ingredients[0]
        assert added_ingredient.name == "Фарш"
        assert added_ingredient.unit == "г"
        assert added_ingredient.quantity == 1415.0

    def test_scale_returns_new_object(self):
        original = Recipe("Пирожки с яблоком", [Ingredient("Мука", 500.0, "г")])
        new = original.scale(2.0)
        assert new is not original
        assert original.ingredients[0].quantity == 500.0  
        assert new.ingredients[0].quantity == 1000.0

    def test_scale_multiplies_quantities(self):
        recipe = Recipe("Компот", [Ingredient("Яблоки", 3.0, "шт"),Ingredient("Сахар", 42.0, "г")])
        scaled = recipe.scale(2.5)
        assert scaled.ingredients[0].quantity == 7.5   
        assert scaled.ingredients[1].quantity == 105.0 

    def test_scale_ratio_validation(self):
        recipe = Recipe("Плов", [Ingredient("Говядина", 1.0, "кг")])
        with pytest.raises(ValueError):
            recipe.scale(0)
        with pytest.raises(ValueError):
            recipe.scale(-5.0)

    def test_len_unique_ingredients(self):
        recipe = Recipe("Летний софт коктейль", [Ingredient("Банан", 1.0, "шт"), Ingredient("Клубника", 1.0, "шт"), Ingredient("Молоко", 200.0, "мл"),Ingredient("Банан", 0.5, "шт")])
        assert len(recipe) == 3
