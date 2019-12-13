from flask import Flask, url_for
from flask import render_template
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)

app.debug = True

#@app.route('/register')

@app.route('/register', methods=['GET', 'POST'])


def choose_flavor():
    if request.method == 'POST':
        flavor = request.form['flavor']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        return redirect(url_for('show_recipes', flavor=flavor, height=height, weight=weight, age=age, gender=gender))
    else:
        return render_template('newindex.html')


@app.route('/fillinfo',methods=['GET','POST'])
def fill_basicinfo():
    if request.method == 'POST':
        #flavor = request.form['flavor']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        print(height,weight,age)
        return redirect(url_for('show_recipes',  height=height, weight=weight, age=age, gender=gender))
    else:
        return render_template('newindex.html')
@app.route('/moveforward',methods=['GET','POST'])
def move_forward():
    if request.method == 'POST':
        return "success"
    else:
        return render_template('index.html')



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
