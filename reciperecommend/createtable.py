"""
@author: xueying peng
"""
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://recipeadm:1234@localhost:3306/recipe_recommendation"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

#创建模型对象


class user_character(UserMixin,db.Model):
    __tablename__='user_character'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    activity = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(120), nullable=False)
    fitnessgoal = db.Column(db.String(120), nullable=False)
    cookingskill = db.Column(db.String(120))
    gender = db.Column(db.String(120), nullable=False)


class user_historicalrecipe(db.Model):
    __tablename__='user_historicalrecipe'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(120),  nullable=False)
    recipeid = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

 #   def __repr__(self):
 #       return '<User %r>' % self.email


db.create_all()
