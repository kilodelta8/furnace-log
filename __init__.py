from flask import Flask, render_template, url_for, flash, session, request, redirect
from flask import Flask, render_template
from flask_wtf import FlaskForm
from sqlalchemy import false, true
from wtforms import Form, StringField, PasswordField, TextAreaField, SubmitField, validators, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
import datetime
import time

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
    # furnaceNum = db.Column(db.Integer)
    # logId = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
    username = db.Column(db.String(30))
    password = db.Column(db.String(250))
    loadingSide = db.Column(db.Boolean(), nullable=False)

    def __init__(self, username, password, loadingSide):
        self.username = username
        self.password = password
        self.loadingSide = loadingSide

    def __repr__(self):
        return self.username


'''
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    furnaceNum = db.Column(db.Integer)
    shift = db.Column(db.Integer)
    glasses = db.Column(db.PickleType, nullable=False)
    jobNum = db.Column(db.PickleType, nullable=False)
    user_name = db.Column(db.String(30))

    def __init__(self, furnaceNum, modelNum, jobNum):
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
    loadingSide = BooleanField(
        'Loading Side', false_values=(False, 0))
    submit = SubmitField('Submit')

# _______________NOT A FORM per say_______________


class LogNavButtons(FlaskForm):
    startTime = SubmitField('Start')
    endTime = SubmitField('Stop')
    pauseTime = SubmitField('Pause')


# ___________________ROUTES_____________________


# home - landing page route


@app.route('/home', methods=['GET', 'POST'])
def home():
    # blog = Blog.query.order_by(Blog.pub_date.desc()).all()

    form = LogNavButtons()
    if form.validate_on_submit():
        # check if any bool is true or false
        if form.startTime.data:
            tm = time.time()
            flash('Now logging time and labels...', 'success')
            print(tm)
            return redirect(url_for('home'))
        elif form.pauseTime.data:
            tm = time.time()
            flash('Logging has been Paused!', 'warning')
            print(tm)
            return redirect(url_for('home'))
        elif form.endTime.data:
            tm = time.time()
            flash('All logging and counts have stopped...', 'danger')
            print(tm)
            return redirect(url_for('home'))
    else:
        return render_template('home.html', title='Furnace Log', form=form)


@app.route('/')
def index():
    return redirect(url_for('login'))


# login to account
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    redirect/render_template <- login(none):
    '''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        hashed = existing_user.password
        # print(existing_user.loadingSide)
        if pbkdf2_sha256.verify(password, hashed):
            session['username'] = existing_user.username
            session['logged_in'] = True
            session['frontOrBack'] = existing_user.loadingSide
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
    '''
    redirect/render_template <- setup(none): A route that displays the setup page to add new users.
    A new user is either load (check box yes), indicating the user will be at the front
    of the furnace or unload (check box unchecked) for the rear unload area of the furnace.
    The position of the user (load/unload) will dictate controls available on the 
    log (home) screen of each user.
    '''
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        loadingSide = request.form.get('loadingSide')
        existing_user = User.query.filter_by(username=username).first()
        if password != verify:
            flash('Your passwords do not match, try again!', 'danger')
            return redirect(url_for('setup'))
        if not existing_user:
            if loadingSide == None:
                loadingSide = False
            else:
                loadingSide = True
            new_user = User(username, pbkdf2_sha256.hash(
                password), loadingSide)
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
    session['frontOrBack'] = None
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
