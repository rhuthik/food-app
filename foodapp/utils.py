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

def alphaKey(ele) :
    return ele.name.lower()

def likeKey(ele) :
    return len(ele.users_liked)

def findRecipe(ingredients, typeOfSearch) :
    result = set()

    for i in Recipe.query.all() :
        result.add(i)

    for ing in ingredients :
        subset = set()
        for i in Ingredient.query.filter_by(name=ing).all() :
            for p in i.recipes :
                subset.add(p)
        result = result.intersection(subset)
    
    ans = list(result)

    if typeOfSearch == 'alpha' :
        ans.sort(key=alphaKey)
        print(ans)
        return ans
    else :
        ans.sort(key=likeKey)
        print(ans)
        return ans


def searching_by_dish_name(dish, ingredients, typeOfSearch) :
    shortList = []
    search = "%{}%".format(dish)
    for i in Recipe.query.filter(Recipe.name.like(search)).all():
        shortList.append(i)

    result = set()

    for i in shortList :
        result.add(i)

    for ing in ingredients :
        subset = set()
        for i in Ingredient.query.filter_by(name=ing).all() :
            for p in i.recipes :
                subset.add(p)
        result = result.intersection(subset)
    
    ans = list(result)

    if typeOfSearch == 'like' :
        ans.sort(key=likeKey, reverse=True)
        print(ans)
        return ans
    else :
        ans.sort(key=alphaKey)
        print(ans)
        return ans

