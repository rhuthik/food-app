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

# Here the list of ingredients selected by the user is passed into the function

def findRecipe(ingredients) :
    result = set()

    for i in Recipe.query.all() :
        result.add(i)

    for ing in ingredients :
        subset = set()
        for i in Ingredient.query.filter_by(name=ing.name).all() :
            for p in i.recipes :
                subset.add(p)
        result = result.intersection(subset)
    
    return result

