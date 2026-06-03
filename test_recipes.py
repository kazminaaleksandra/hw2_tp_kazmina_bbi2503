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


class TestShoppingList:
    def test_add_recipe_success(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Пышный омлет", [Ingredient("Яйца", 3.0, "шт"),Ingredient("Молоко", 50.0, "мл")])
        shopping_list.add_recipe(recipe, portions = 2)
        res = shopping_list.get_list()
        assert len(res) == 2
        
    def test_add_recipe_invalid_portions(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Лазанья", [Ingredient("Томаты", 1.0, "шт")])
        with pytest.raises(ValueError):
            shopping_list.add_recipe(recipe, portions = 0 )
        with pytest.raises(ValueError):
            shopping_list.add_recipe(recipe, portions= -5)
    
    def test_remove_recipe_existing(self):
        shopping_list = ShoppingList()
        recipe1 = Recipe("Борщ", [Ingredient("Свекла", 2.0, "шт"), Ingredient("Капуста", 365.0, "г")])
        recipe2 = Recipe("Битые огурцы", [Ingredient("Огурец", 3.0, "шт")])
        shopping_list.add_recipe(recipe1, portions=1)
        shopping_list.add_recipe(recipe2, portions=1)
        shopping_list.remove_recipe("Борщ")
        res = shopping_list.get_list()
        assert len(res) == 1
        assert res[0].name == "Огурец"
    
    def test_remove_recipe_not_existing(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Пюре", [Ingredient("Картошка", 500.0, "г")])
        shopping_list.add_recipe(recipe, portions=1)
        shopping_list.remove_recipe("Рецепт не найден")
        assert len(shopping_list.get_list()) == 1
    
    def test_get_list_ingredient_merging (self):
        shopping_list = ShoppingList()
        recipe1 = Recipe("Рисовая каша", [Ingredient("Молоко", 200.0, "мл")])
        recipe2 = Recipe("Кофе", [Ingredient("Молоко", 50.0, "мл")])
        shopping_list.add_recipe(recipe1, portions=1)
        shopping_list.add_recipe(recipe2, portions=1)
        res = shopping_list.get_list()
        assert len(res) == 1
        assert res[0].name == "Молоко"
        assert res[0].quantity == 250.0
    
    def test_get_list_sorted_by_name(self):
        shopping_list = ShoppingList()
        recipe = Recipe("Тесто", [Ingredient("Яйца", 3.0, "шт"),Ingredient("Мука", 500.0, "г"), Ingredient("Сахар", 200.0, "г")])
        shopping_list.add_recipe(recipe, portions= 1)
        res = shopping_list.get_list()
        names = [ingredient.name for ingredient in res]
        assert names == sorted(names)  
        assert names == ["Мука", "Сахар", "Яйца"]
    
    def test_add_combine_lists(self):
        list1 = ShoppingList()
        list2 = ShoppingList()
        recipe1 = Recipe("Блины", [Ingredient("Мука", 500.0, "г")])
        recipe2 = Recipe("пышный омлет", [Ingredient("Яйца", 3.0,"шт")])
        list1.add_recipe(recipe1, portions = 1)
        list2.add_recipe(recipe2, portions = 1)
        mixed = list1 + list2
        res = mixed.get_list()
        assert len(res) == 2
        ingredients = {ingredient.name: ingredient.quantity for ingredient in res}
        assert ingredients["Мука"] == 500.0
        assert ingredients["Яйца"] == 3.0
    
    def test_add_immutable(self):
        list1 = ShoppingList()
        list2 = ShoppingList()
        recipe = Recipe("Крамбл кукис", [Ingredient("Корица", 10.0, "г")])
        list1.add_recipe(recipe, portions = 1)
        list2.add_recipe(recipe, portions = 2)
        len1_before = len(list1.get_list())
        len2_before = len(list2.get_list())
        mixed = list1 + list2
        assert len(list1.get_list()) == len1_before
        assert len(list2.get_list()) == len2_before
        assert mixed.get_list()[0].quantity == 30.0
