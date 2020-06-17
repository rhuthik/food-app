from ..foodapp.utils import findRecipe

search = [Ingredient.query.get(5)]

for i in findRecipe(search) :
    print(f"{i.name} ")
