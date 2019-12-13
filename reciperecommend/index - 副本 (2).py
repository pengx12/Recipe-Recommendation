from flask import Flask, url_for
from flask import render_template
import flask

from flask_login import LoginManager
from flask_login import login_user, login_required
from . import connsql
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://recipeadm:1234@localhost:3306/recipe_recommendation"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


connsql.db.init_app(app)
#@app.route('/register')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('newindex.html')
@app.route('/chooseflavour',methods=['GET', 'POST'])
def choose_flavor():
    if request.method == 'POST':
        flavor = request.form['flavor']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        return redirect(url_for('show_recipes', flavor=flavor, height=height, weight=weight, age=age, gender=gender))
    else:
        print ('asdfsf')
        return render_template('newindex.html')


@app.route('/fill_basicinfo',methods=['GET','POST'])
def fill_basicinfo():
    if request.method == 'POST':
        #flavor = request.form['flavor']
        user = request.form['user']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        print(height,weight,age)
        user = connsql.User(username='yujiujiu2', password='11111')
        connsql.db.session.add(user)
        connsql.db.session.commit()
        return redirect(url_for('show_recipes',  height=height, weight=weight, age=age, gender=gender))
    else:
        return render_template('newindex.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # flavor = request.form['flavor']
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        pwd2 = request.form['password2']
        print(name, email, pwd)
        user=connsql.User.query.filter(connsql.User.email==email).first()
        #判断用户名是否存在
        if user:
            return u' email existed'
        else:
            user = connsql.User(username=name, password=pwd, email=email)
            connsql.db.session.add(user)
            connsql.db.session.commit()
            return redirect(url_for('index', user=user))
            return "success"
    else:
        return render_template('newindex.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # flavor = request.form['flavor']
        email = request.form['email']
        pwd = request.form['password']
        print(email, pwd)
        #user = connsql.User(username=name, _password=pwd, email=email)
        #connsql.db.session.add(user)
        #connsql.db.session.commit()

        return redirect(url_for('index'))
        return "success"
    else:
        return render_template('newindex.html')


@app.route('/moveforward',methods=['GET','POST'])
def move_forward():
    if request.method == 'POST':
        return "success"
    else:
        return render_template('newindex.html')



@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
    app.run()
