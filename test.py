from foodapp.utils import *

search = [Ingredient.query.get(5)]

for i in findRecipe(search) :
    print(f"{i.name} ")
