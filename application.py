# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
import constraint
import ast

from settings import APP_STATIC

import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

application = Flask(__name__)
application.debug = True

mysql = MySQL()
"""
application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'FriApr14'
application.config['MYSQL_DATABASE_DB'] = 'recipe'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
"""
application.config['MYSQL_DATABASE_USER'] = 'flourishlove'
application.config['MYSQL_DATABASE_PASSWORD'] = 'MonApr17'
application.config['MYSQL_DATABASE_DB'] = 'recipe'
application.config['MYSQL_DATABASE_HOST'] = 'reciperecommendation.cky4qlh0i2dz.us-east-1.rds.amazonaws.com'
#application.config['MYSQL_DATABASE_PORT'] = 3306

mysql.init_app(application)

@application.route('/show')
def show_recipes():
    cur_flavor = request.args.get('flavor')
    cur_height = float(request.args.get('height'))/100
    cur_weight = request.args.get('weight')
    cur_age = request.args.get('age')
    cur_gender = request.args.get('gender')
    cur_activity = request.args.get('activityLevel')
    #cur.execute("SELECT name FROM recipes WHERE flavor = %s;", [cur_flavor])
    if cur_flavor == 8:
        flavor_name = "Slow Cooker Irish Beef Stew"
    elif cur_flavor == 7:
        flavor_name = "Cilantro Lime Chicken Tacos"
    elif cur_flavor == 6:
        flavor_name = "Shumai with Crab and Pork"
    elif cur_flavor == 5:
        flavor_name = "Cuban Style Lamb"
    elif cur_flavor == 4:
        flavor_name = "Southwestern Beef Wraps"
    elif cur_flavor == 3:
        flavor_name = "Chicken and Avocado Burritos"
    elif cur_flavor == 2:
        flavor_name = "Chicken Stir-Fry with Noodles"
    elif cur_flavor == 1:
        flavor_name = "Mexican Beef Lasagna"
    else:
        flavor_name = "Asian Garlic Tofu"

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT num, nutrition FROM recipe_info WHERE dbscan_label = %s;", [cur_flavor])
    fetch_result = cur.fetchall()
    satisfied_recipes = constraint.nutritional_constraints(fetch_result, cur_age, cur_weight, cur_height, cur_gender, 'Active')
    print (satisfied_recipes)
    # provider, big_image
    error = None
    entries = []
    count = 0
    for group in satisfied_recipes:
        templist = []
        for i in range(0,3):
            cur.execute("SELECT name, cuisine, provider, big_image, ingredient_amount FROM recipe_info WHERE num = %s and dbscan_label = %s;", [group[i], cur_flavor])
            temp = cur.fetchall()
            print (temp)
            templist.append(temp)
        entries.append(templist)
        count = count + 1
        if count > 3:
            break
    conn.close()
    #return render_template('content.html', entries=entries, error=error)
    return render_template('recipeRecommend.html', entries=entries, error=error)
"""
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipe_info WHERE dbscan_label = %s;", [cur_flavor])
        fetch_result = cur.fetchall()
        entries = constraint.nutritional_constraints(fetch_result, cur_age, cur_weight, cur_height, cur_gender, 'Active')
        print entries
        conn.close()
        error = None
        return render_template('content.html', entries=entries, error=error)
    except Exception as e:
        print str(e)
        entries = None
        error = 'Database Connection Error!'
        return render_template('content.html', entries=entries, error=error)
"""


@application.route('/', methods=['GET', 'POST'])
def choose_flavor():
    if request.method == 'POST':
        flavor = request.form['flavor']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        return redirect(url_for('show_recipes', flavor=flavor, height=height, weight=weight, age=age, gender=gender))
    else:
        return render_template('index.html')


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
