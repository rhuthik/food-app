from foodapp import db
from foodapp.models import Recipe, Ingredient
import json

db.create_all()

with open('foodapp/static/train.json') as json_file:
    data = json.loads(json_file.read())
    for recipe in data:
        rec = Recipe(name=recipe['cuisine'], procedure="lorem ipsum")
        db.session.add(rec)
        db.session.commit()
        for ing in recipe['ingredients']:
            ingre = Ingredient(name=ing)
            db.session.add(ingre)
            db.session.commit()
            rec.ingredients.append(ingre)
            db.session.commit()
                    
