from foodapp import db
from foodapp.models import Recipe, Ingredient
import json

db.drop_all()
db.create_all()

with open('seed-resource/train.json') as json_file:
    data = json.loads(json_file.read())
    for recipe in data:
        rec = Recipe(name=recipe['cuisine'], procedure="lorem ipsum")
        db.session.add(rec)
        db.session.commit()
        for ing in recipe['ingredients']:

            ingList = Ingredient.query.filter_by(name=ing).all()

            if len(ingList) == 1 :
                rec.ingredients.append(ingList[0])
            
            else :
                ingre = Ingredient(name=ing)
                db.session.add(ingre)
                db.session.commit()
                rec.ingredients.append(ingre)
                db.session.commit()