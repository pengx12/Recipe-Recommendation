from flask import Flask,render_template
from flask_pymongo import PyMongo
import constraint
import ast
app = Flask(__name__)
#实例化数据库配置，可以直接一行解决
app.config["MONGO_URI"]="mongodb://localhost:27017/recipe"
mongo = PyMongo(app)

#也可以两行来实例化配置,这里会把所有以MONGO开头的配置加入。
class MongoDB():
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DBNAME = "recipe"
#app.config.from_object(MongoDB)
#mongo.init_app(app,config_prefix="MONGO%")
def firstinsert():
    recitable=mongo.db.recipeinfo
    reci = mongo.db.recipeinfo.find_one({"cuisine":"Chinese"})
    reci = mongo.db.recipeinfo.find_one()

    print((reci,reci["cuisine"]))
    print (reci["cuisine"])
    print ('asdfadsf')
    res=recitable.find({"cuisine":"Chinese", "dbscan_label":2})
    arr=[]
    recipearr=[]
    for x in res:
        #print (x)
        arr.append((x["_id"],x["nutrition"]))
        recipearr.append((x["id"],x["name"],x["big_image"],x["ingredient_amount"],x["provider"]))
    for i in range(9,20):
        x=recipearr[i]
        recipe = {
            'recipeid': x[0],
            'name': x[1],
            'imgurl': x[2],
            'ingredient': x[3],
            'provider': x[4]
        }
        mongo.db.recommendingrecipe.insert(recipe)
#print (satisfied_recipes)
def updatenutritionconstraint():

    recitable=mongo.db.recipe_clusternutrition
    arr = recitable.find()
    nutrition_list = ['ENERC_KJ', 'PROCNT', 'CHOCDF', 'FIBTG', 'FAT', 'CA', 'FE', 'MG', 'P', 'K', \
                      'NA', 'ZN', 'MN', 'SE', 'VITA_RAE', 'TOCPHA', 'VITC', 'RIBF', 'NIA', 'VITB6A', 'BITB12'
        , 'CHOLN', 'VITK', 'FOL']
    unit_ratio = [1, 1, 1, 1, 1, 1000, 1000, 1000, 1000, 1000, \
                  1000, 1000, 1000, 1000000, 0.001, 1000, 1000, 1000, 1000, 1000, 1000000
        , 1000, 1000000, 1000000]
    for x in arr:
        n_nutrition = len(nutrition_list)
        my_nutrition = [0 for i in range(n_nutrition)]
        temp_list = ast.literal_eval(x["nutrition"])  # convert unicode to python list of dictionary
        for element in temp_list:
            for i in range(n_nutrition):
                if element['attribute'] == nutrition_list[i]:
                    my_nutrition[i] = element['value'] * unit_ratio[i]  # /recipe[14]
        recitable.update({"id": x["id"]}, {"$set": {"nutrition_list": my_nutrition}})
updatenutritionconstraint()