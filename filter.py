from foodapp import db
from foodapp.models import *

# ------------ For shortlisting the ingredients based on user's search query ----------------

def filterIngredients(string) :
    filtered_list = []
    for i in Ingredient.query.all() :
        if (i.name).find(string) != -1 :
            filtered_list.append(i)
    return filtered_list

# -------------------------------------------------------------------------------------------

# ------------- For filtering the recipes corresponding to ingredients selected -------------

def findRecipe(ingred) :
    subset = set()

    for i in Ingredient.query.filter_by(name=ingred.name).all() :
        global result
        for p in i.recipes :
            subset.add(p)
        
    result = result.intersection(subset)

# -------------------------------------------------------------------------------------------


search = [Ingredient.query.get(5)]

result = set()


for i in Recipe.query.all() :
    result.add(i)

for i in search :
    findRecipe(i)


for i in result :
    print(f"{i.name} ")


