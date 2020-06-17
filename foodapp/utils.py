from foodapp import db
from foodapp.models import *

# ------------ For shortlisting the ingredients based on user's search query ----------------

def filter(string) :
    shortList = []
    search = "%{}%".format(string)
    count = 0
    for ing in Ingredient.query.filter(Ingredient.name.like(search)).all() :
        count += 1
        shortList.append(ing.name)
        
        if count == 10 :
            break
    
    return shortList

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

