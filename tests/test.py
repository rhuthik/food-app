import sys
sys.path.insert(0, '..')
from foodapp.utils import db, Ingredient, Recipe, findRecipe

search = [Ingredient.query.get(5)]

for i in findRecipe(search) :
    print(f"{i.name} ")
