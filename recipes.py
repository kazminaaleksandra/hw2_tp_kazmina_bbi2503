class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value > 0:
            self._quantity =  value
        else:
            raise ValueError(
                "Количество должно быть положительным"
            )

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient: Ingredient):
        for added in self.ingredients:
            if added == ingredient:
                added.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            return float(ratio) > 0
        except (ValueError, TypeError):
            return False

    def scale(self, ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError(
                f"Некорректное соотношение: {ratio}"
            )
        scaled_ingredients = [
            Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit)
            for ingredient in self.ingredients
        ]
    
        return Recipe(self.title, scaled_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        required_ingredients = "\n".join(f"{i+1}. {ingredient}" for i, ingredient in enumerate(self.ingredients))
        return f"{self.title}, required ingredients: {required_ingredients}"
    
 class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients = None):
        if ingredients is None:
            ingredients = []
        self.diet_type = diet_type
        super().__init__(title, ingredients)

    def scale(self, ratio:float):
        adjusted_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, adjusted_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"       
        
        
