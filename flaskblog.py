from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eca8e1a76a40261da1c8ba172bb99630'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'site.db')

db = SQLAlchemy(app)

app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship("Post", backref = "author", lazy = True)

    def __repr__(self):
        return f"user('{self.username}','{self.email}', '{self.image_file}')"
    
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"post('{self.title}', '{self.date_posted}')"

    def __init__(self,title,content):
        self.title = title
        self.content = content


posts = [
    {
        
        "author" : "dishant",
        "title" : "Blog post 2",
        "content": "First post content",
        "date": "22 dec 2023"
    },
    {
       
        "author" : "shiv",
        "title" : "Blog post 1",
        "content": "Second post content",
        "date": "12 march 2023"
    }
]


@app.route("/")
def hello():
    return "<h5>hello world!</h5>"

@app.route("/about")
def about():
    return render_template("about.html", title = "about")

@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', "success")
        return redirect(url_for('home'))
    return render_template("register.html", title = 'Register', form= form )

@app.route("/login",  methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == 'password':
            flash("You have been logged in! ", 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title = "Login", form = form)

if __name__  ==  "__main__":
    app.run(debug = True)