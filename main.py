from functools import wraps
import json
from flask import Flask, render_template, request, session, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime

import math

app = Flask(__name__)
app.secret_key = 'your_secret_key'
local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

#SNo,Name,  BodyPart,Equipment,Video-URL,Content,Slug
class Post(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    BodyPart = db.Column(db.String(20), nullable=False)
    Equipment = db.Column(db.String(50), nullable=False)
    Content = db.Column(db.String(300), nullable=False)
    Video_URL = db.Column(db.String(50), nullable=True)
    Slug = db.Column(db.String(50), nullable=False)

#SNo,Name,email,password,age,weight,height,gender

class User(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train1/equip")
def train_no_equip():
    posts = Post.query.filter(Post.Equipment != 'No Equipment').all()
    return render_template("equipment2.html", posts=posts)

@app.route("/train2/no_equip")
def train_equip():
    posts = Post.query.filter_by(Equipment='No Equipment').first()

    return render_template("equipment3.html", posts=posts)

@app.route("/train1/equip/<string:post_BodyPart>", methods=['GET'])
def train2(post_BodyPart):
    posts = Post.query.filter(Post.BodyPart == post_BodyPart, Post.Equipment != 'No Equipment').first()
    return render_template("equipment2.html", posts=posts)

@app.route("/train2/no_equip/<string:post_BodyPart>",methods=['GET'])
def train3(post_BodyPart):
    posts = Post.query.filter_by(BodyPart=post_BodyPart,Equipment='No Equipment').first()
    return render_template("equipment3.html", posts=posts)

@app.route("/post/<string:post_slug>",methods=['GET'])
def equipment(post_slug):
    posts = Post.query.filter_by(Slug=post_slug).first()
    return render_template("equipment.html", posts=posts)

#SNo,Name,email,password,age,weight,height,gender


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('sex')
        age = request.form.get('age')
        height = request.form.get('height')
        weight = request.form.get('weight')

        user = User(Name=name, email=email, password=password, age=age, weight=weight, height=height, gender=gender)
        db.session.add(user)
        db.session.commit()

        session['email'] = email  # Set the session email
        return redirect(url_for('user'))  # Redirect to index.html

    return render_template('signup.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def login():
    if "email" in session:
        return redirect(url_for('user'))  # Redirect to index.html if user is already logged in
    
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['email'] = email
            return redirect(url_for('user'))  # Redirect to index.html after successful login
        else:
            return 'Invalid email or password'

    return render_template('login.html')


@app.route('/user',methods=['GET','POST'])
def user():
    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in
    return render_template('user.html')

@app.route('/logout')
def logout():
    session.pop('email', None)  # Remove 'email' from session if it exists
    return redirect(url_for('index'))  # Redirect to index.html after logout

if __name__ == "__main__":
    app.run(debug=True)
