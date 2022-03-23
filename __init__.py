from myImports import *


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


# TODO - develop a model for a log sheet, suitable for a DB
'''
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now(datetime.timezone.utc))
    furnaceNum = db.Column(db.Integer)
    shift = db.Column(db.Integer)
    glasses = db.Column(db.PickleType(mutable=True), nullable=False)
    jobNum = db.Column(db.PickleType(mutable=True), nullable=False)
    checks = db.Column(db.PickleType(mutable=True), nullable=False)
    user_name = db.Column(db.String(45))

    def __init__(self, furnaceNum):
        self.furnaceNum = furnaceNum

    def getLogInMatrixOrder(self):
        for x in range(31):  # up to 31 glass models
            print(self.glasses[x] + "  A" + self.jobNum[x] + " ")
            for y in range(21):
                # print each glass model with four spaces then
                print(self.checks[x][y] + " ")

    def __repr__(self):
        return self.furnaceNum
'''

# ------------GLOBALS--------------
furnaces = [20]
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
    change = SubmitField("Change")
    add = SubmitField("add")
    remove = SubmitField("Remove")
    other = SubmitField("Other")
    print = SubmitField("print")
    startBtnClicked = None
    pauseBtnClicked = None
    pauseBtnCounter = None

    def setStartClicked():
        if startClicked == 0:
            startClicked = 1

    def resetStartClicked():
        if startClicked == 1:
            startClicked = 0

    def isStartClicked():
        if startClicked == 1:
            return True
        else:
            return False

        # ___________________ROUTES_____________________

        # home - landing page route


@app.route('/home', methods=['GET', 'POST'])
def home():
    '''
    home(None) route.
    '''
    # blog = Blog.query.order_by(Blog.pub_date.desc()).all() <-left for DB query reference

    # instantiate an instance of the LogNavButtons class
    form = LogNavButtons()

    # check for post request, if so: Which button posted the request?
    if request.method == 'POST':

        # TODO - startTime grabs an instance of time as a starting point for logging of label counts
        if request.form.get('startTime', '') == 'Start':
            tm = time.time()
            flash('Now logging time and labels... ' +
                  str(tm), 'success')
            # form.setStartClicked()
            return redirect(url_for('home'))

        # TODO - pauseTime grabs two instances of time (at a time), disabling all else until the second click, subtracting
        # the two and storing the total time for later subtraction from the total logging time.
        elif request.form.get('pauseTime', '') == 'Pause':
            tm = time.time()
            flash('Logging has been Paused!' +
                  str(((tm / 1000) / 60) / 60), 'warning')
            # if the remainder of session['pauseBtnCounter'] equals 0, then the var is even
            # thus, a beginning and end pause time has been recorded and the session var can
            # be set to True to start a third pause session
            pauseCount = session['pauseBtnCounter']
            if pauseCount % 2 == 0:
                session['pauseBtnClicked'] = True
                session['pauseBtnCounter'] = pauseCount + 1
            return redirect(url_for('home'))

        # TODO - endTime grabs the last timestamp in the equation to decide total time for the calculation of total labels
        elif request.form.get('endTime', '') == 'Stop':
            tm = time.time()
            flash('All logging and counts have stopped...' +
                  str(((tm / 1000) / 60) / 60), 'danger')
            session['startBtnClicked'] = False
            return redirect(url_for('home'))

        # TODO - change presents a popup menu to enter the information for a new model for a mold change or print change
        # then updates the DB and present the last label count for the prior model
        elif request.form.get('change', '') == 'Change':
            tm = time.time()
            flash('Change is working...', 'success')
            return redirect(url_for('home'))

        # TODO - add presents a pop up menu to add glass (should be in A setup menu)
        elif request.form.get('add', '') == 'Add':
            flash('Add button is working', 'success')
            return redirect(url_for('home'))

        # TODO - remove may be redundant and not necassary (if so, should be in A setup menu)
        elif request.form.get('remove', '') == 'Remove':
            flash('Remove button is working', 'success')
            return redirect(url_for('home'))

        # TODO - other.....for what????
        elif request.form.get('other', '') == 'Other':
            flash('Other button is working', 'success')
            return redirect(url_for('home'))

        # TODO - should this be here??  Pretty sure this is a whole 'nother world
        elif request.form.get('print', '') == 'Print':
            flash('Print button is working', 'success')
            return redirect(url_for('home'))

    # If not post then get
    return render_template('home.html', title='Furnace Log', form=form)


# TODO - can this route be placed underneath the /login route???
@app.route('/')
def index():
    return redirect(url_for('login'))


# login to account
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    login(None) route.  This method allows a user to login to the system.
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
            session['startBtnClicked'] = False
            session['pauseBtnClicked'] = False
            session['pauseBtnCounter'] = int(0)
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
            session['startBtnClicked'] = False
            session['pauseBtnClicked'] = False
            session['pauseBtnCounter'] = int(0)
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
