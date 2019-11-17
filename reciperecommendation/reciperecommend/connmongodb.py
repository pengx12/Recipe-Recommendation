"""
@author: xueying peng
"""
from flask import Flask,render_template
from flask_pymongo import PyMongo
import numpy as np
from . import Nutrition_Extraction
from . import constraint
#app = Flask(__name__)
#实例化数据库配置，可以直接一行解决
#app.config["MONGO_URI"]="mongodb://localhost:27017/recipe"
mongo = PyMongo()

#也可以两行来实例化配置,这里会把所有以MONGO开头的配置加入。
class MongoDB():
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DBNAME = "recipe"
#app.config.from_object(MongoDB)
#mongo.init_app(app,config_prefix="MONGO%")
def getSatisifiedRecipe():
    recipe=mongo.db.recommendingrecipe
    res=recipe.find()
    arr=[]
    tmp=[]
    resarr=[]
    for x in res:
        arr.append((x["recipeid"],x["name"],x["ingredient"],x["provider"],x["imgurl"]))
    i=0
    while i<len(arr):
        tmp.append(arr[i])
        if i%3==2:
            resarr.append(tmp)
            tmp=[]
        i=i+1
    return resarr

def getSatisifiedRecipefrommongo(email,region,character):
    recipe=mongo.db.recommendingrecipe
    res=recipe.find({"email": email})
    if not res:
        writeSatisifiedRecipeintoMongo(email, None, region, character)
        res = recipe.find({"email": email})
    return res
def writeSatisifiedRecipe():
    recitable=mongo.db.recipeinfo
    reci = mongo.db.recipeinfo.find_one({"cuisine":"Chinese"})
    reci = mongo.db.recipeinfo.find_one()
    print((reci,reci["cuisine"]))
    res=recitable.find({"cuisine":"Chinese", "dbscan_label":2})
    arr=[]
    recipearr=[]
    for x in res:
        #print (x)
        arr.append((x["_id"],x["nutrition"]))
        recipearr.append((x["id"],x["name"],x["big_image"],x["ingredient_amount"],x["provider"]))
    for i in range(1,9):
        x=recipearr[i]
        recipe = {
            'recipeid': x[0],
            'name': x[1],
            'imgurl': x[2],
            'ingredient': x[3],
            'provider': x[4]
        }
        mongo.db.recommendingrecipe.insert(recipe)

def getflavourres(recipe,region):
    recitable=mongo.db.recipe_clusternutrition
    db90lab=set()
    db40lab=set()
    hirlab=set()
    regionlab=set()
    regionlab.add(region)
    db90res=set()
    res=[]
    hirres=set()
    if recipe:
        for x in recipe:
            idres= recitable.find_one({"id": x})
            db90lab.add(idres['db90type'])
            db40lab.add(idres['db40type'])
            hirlab.add(idres['hie_label'])
            regionlab.add(idres['cuisine'])
        for x in db90lab:
            arr=recitable.find({"db90type": x})
            for y in arr:
                if y["id"] not in recipe and y["id"] not in db90res:
                    db90res.add(y["id"])
                    res.append([y["id"],y["nutrition_list"]])
        n = len(db90res) / 3
        for x in hirlab:
            for y in regionlab:
                arr = recitable.find({"hie_label": x, "cuisine": y})
                i=0
                for z in arr:
                    if i>n:
                        break
                    i+=1
                    if z["id"] not in recipe and z["id"] not in db90res:
                        db90res.add(z["id"])
                        res.append([z["id"], z["nutrition_list"]])
    else:
        arr = recitable.find({"cuisine": region})
        if arr:
            for z in arr:
                res.append([z["id"], z["nutrition_list"]])
        else:
            arr=recitable.find()
            for z in arr:
                res.append([z["id"], z["nutrition_list"]])
    return res
def writeSatisifiedRecipeintoMongo(email, recipe, region,character):
    db90res=getflavourres(recipe,region)
    np.random.shuffle(db90res)
    recipeinfo=mongo.db.recipeinfo
    print (len(db90res))
    ingarr=[]
    recipearr=[]
    satisfiedlst=constraint.nutritional_constraints(db90res, character.age,character.weight, character.height, character.gender, character.activity,character.fitnessgoal)
    #standard = nutrition(character.age,character.weight, character.height, character.gender, character.activity)
        #print (x)
#        arr.append((x["_id"],x["nutrition"]))
#        recipearr.append((x["id"],x["name"],x["big_image"],x["ingredient_amount"],x["provider"]))
    recommendingrecipe=mongo.db.recommendingrecipe
    x=recommendingrecipe.delete_many({"email": email})
    #print (x.deleted_count)
    for y in satisfiedlst:
        arr=[]
        for x in y:
            rec=recipeinfo.find_one({"id": x})
            tmp = {
                'recipeid': x,
                'name': rec['name'],
                'imgurl': rec['big_image'],
                'ingredient': rec["ingredient_amount"],
                'provider': rec['provider']
            }
            arr.append(tmp)
        recipe = {
            'email': email,
            'recipearr': arr
        }
        recommendingrecipe.insert(recipe)
    rres=getSatisifiedRecipefrommongo(email, region, character)
    a=rres[0]['recipearr'][0]['imgurl']
    print (rres)