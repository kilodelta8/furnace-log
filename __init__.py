from flask import Flask, render_template, url_for, flash, session, request, redirect
from flask import Flask, render_template
from wtforms import Form, StringField, PasswordField, TextAreaField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
#from datetime import datetime
import json
import urllib3


# application init and configurations
app = Flask(__name__)

# with open('/etc/config.json') as config_file:
#    config = json.load(config_file)

# TODO - change to environment variable
app.config['SECRET_KEY'] = 'fuyao123'  # config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://fuyao@localhost:3306/fuyao"
app.config['SQLALCHEMY_ECHO'] = True

# initialize instance of db
db = SQLAlchemy(app)


# ---------------MODELS--------------------
# TODO finish model befores instantiation
# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #logId = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
    username = db.Column(db.String(30))
    password = db.Column(db.String(250))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username


'''
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    furnaceNum = db.Column(db.Integer)
    modelNum = db.Column(db.Integer)
    jobNum = db.Column(db.Integer)
    numOfWagon = db.Column(db.Integer)
    user = db.relationship('User', backref='log', lazy=True)

    def __init__(self, furnaceNum, modelNum, jobNum, numOfWagon):
        self.furnaceNum = furnaceNum
        self.modelNum = modelNum
        self.jobNum = jobNum
        self.numOfWagon = numOfWagon

    def __repr__(self):
        return self.furnaceNum

'''
# ____________________FORMS______________________
# Login form


class LoginForm(Form):
    username = StringField('Username', [validators.Length(
        min=6, max=30), validators.DataRequired()])
    password = PasswordField(
        'Password', [validators.Length(min=7), validators.DataRequired()])
    submit = SubmitField('Submit')


# Registration form
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(
        min=6, max=30), validators.DataRequired()])
    password = PasswordField(
        'Password', [validators.Length(min=7), validators.DataRequired()])
    verify = PasswordField('Verify Password', [validators.DataRequired()])
    submit = SubmitField('Submit')


# ___________________ROUTES_____________________


# home - landing page route
@app.route('/home')
def home():
    #blog = Blog.query.order_by(Blog.pub_date.desc()).all()
    return render_template('home.html', title='Furnace Log')

# login to account


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        hashed = existing_user.password
        if pbkdf2_sha256.verify(password, hashed):
            session['username'] = existing_user.username
            session['logged_in'] = True
            # TODO - write js to fade out alert
            flash('You are now logged in!', 'success')
            return redirect(url_for('home'))
        elif not existing_user:
            flash('Error with your username!', 'danger')
            return redirect(url_for('login'))
        else:
            flash('Password is incorrect', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Login!', form=form)


# signup for an account
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        if password != verify:
            flash('Your passwords do not match, try again!', 'danger')
            return redirect(url_for('setup'))
        if not existing_user:
            new_user = User(username, pbkdf2_sha256.hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            session['logged_in'] = True
            return redirect(url_for('home'))
        elif len(existing_user) > 0:
            flash('That username is already in use, try again!', 'danger')
            return redirect(url_for('setup'))
    else:
        return render_template('setup.html', title='Setup User', form=form)


# logout user
@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))


@app.before_request
def require_login():
    allowed_routes = ['login', 'setup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


# <<<-------------------------------------------------------->>>
if __name__ == '__main__':
    app.run(debug=True)
