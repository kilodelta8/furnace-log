# import everything (*) from myImports.py
from myImports import *


# application initialization and configurations
app = Flask(__name__)

# TODO - when in actual priduction use, use an outside file for security
# or use (*argv, **kwarg) to handle app password security
# with open('/etc/config.json') as config_file:
#    config = json.load(config_file)

# TODO - change to environment variable
app.config['SECRET_KEY'] = 'fuyao123'  # config.get('SECRET_KEY') SEE ABOVE to do
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://fuyao@localhost:3306/fuyao"
app.config['SQLALCHEMY_ECHO'] = True

# initialize instance of db
db = SQLAlchemy(app)


# ---------------MODELS--------------------
# TODO finish model befores instantiation
# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    furnaceNum = db.Column(db.Integer)
    furnaceSpeed = db.Column(db.Integer)
    wagonCount = db.Column(db.Integer)
    # logId = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
    username = db.Column(db.String(30))
    password = db.Column(db.String(250))
    loadingSide = db.Column(db.Boolean(), nullable=False)
    log = db.relationship('Log', backref='user', lazy=True)

    def __init__(self, username, password, furnNum, loadingSide):
        self.username = username
        self.password = password
        self.furnaceNum = furnNum
        self.loadingSide = loadingSide

    def __repr__(self):
        return self.username


# glass model
class Glass(db.Model):
    glassNum = db.Column(db.String(15), primary_key=True)
    jobNum = db.Column(db.String(7))
    ADASmeasure = db.Column(db.String(12), nullable=True)
    measurement = db.Column(db.String(8))

    def __init__(self, glassnum, jobnum, adas, measure):
        self.glassNum = glassnum
        self.jobNum = jobnum
        self.ADASmeasure = adas
        self.measurement = measure

    def __repr__(self):
        return self.glassNum



# Log db model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    speed = db.Column(db.Integer)
    cols = db.Column(db.Integer)
    wagons = db.Column(db.Integer)
    # glass array with an array of checkmarks (pickletype???)
    def __init__(self, userid, spd, wags):
        self.user_id = userid
        self.speed = spd
        self.wagons  = wags



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
    furnaceNumber = StringField('Furnace Number', [validators.length(
        min=1, max=2), validators.DataRequired()])
    loadingSide = BooleanField(
        'Loading Side', false_values=(False, 0))
    submit = SubmitField('Submit')



# Settings form
class SettingsForm(Form):
    wagonCount = StringField('Wagon Count', [validators.Length(min=2, max=2)])
    furnaceNum = StringField('Furnace Number', [validators.Length(min=1, max=2)])
    speed = StringField('Speed', [validators.Length(min=1, max=2), validators.DataRequired()])
    submit = SubmitField('Update')


# start of shit form
class StartForm(Form):
    wagonCount = StringField('Wagon Count', [validators.Length(min=2, max=2), validators.DataRequired()])
    speed = StringField('Speed', [validators.Length(min=1, max=2), validators.DataRequired()])
    furnaceNum = StringField('Furnace Number', [validators.Length(min=1, max=2), validators.DataRequired()])


# glass add form
class GlassForm(Form):
    modelNum = StringField('Model Number', [validators.Length(min=6, max=11), validators.DataRequired()])
    jobNum = StringField('Job Number', [validators.Length(min=6, max=7), validators.DataRequired()])
    adas = StringField('ADAS', [validators.Length(min=4, max=10)])
    measure = StringField('Measurements', [validators.Length(max=7), validators.DataRequired()])



class LogNavButtons(FlaskForm):
    startTime = SubmitField('Start')
    endTime = SubmitField('Stop')
    pauseTime = SubmitField('Pause')
    change = SubmitField("Change")
    add = SubmitField("add")
    remove = SubmitField("Remove")
    other = SubmitField("Other")
    print = SubmitField("print")




# ___________________ROUTE FUNCTIONS_____________________


# beginning of shift start form route
@app.route('/start', methods=['GET', 'POST'])
def start():
    form = StartForm(request.form)
    if request.method == 'POST' and form.validate():
        wagoncount = request.form['wagonCount']
        spd = request.form['speed']
        furnacenum = request.form['furnaceNum'] 
        username = session['username']
        existing_user = User.query.filter_by(username=username).first()
        new_log = Log(existing_user.id, spd, wagoncount)
        db.session.add(new_log)
        existing_user.furnaceNum = furnacenum
        db.session.commit()
        tm = time.time()
        flash('Now logging time and labels at: ' +
                parseTime(str(time.ctime(tm))), 'success')
        session['startTime'] = str(tm)
        session['startBtnClicked'] = True
        furnace.writeToLog("Start button clicked.")
        flash('Your shift has now started!', 'success') 
        return redirect(url_for('home'))     
    return render_template('start.html', title="Start of Shift", form=form)



# home - main logging page route
@app.route('/home', methods=['GET', 'POST'])
def home():
    '''
    home(none) route.
    '''
    # left for reference, when we start pulling from the db
    # blog = Blog.query.order_by(Blog.pub_date.desc()).all() <-left for DB query reference

    # instantiate an instance of the LogNavButtons class
    form = LogNavButtons()

    # check for post request, if so: Which button posted the request?
    if request.method == 'POST':

        # grabs two instances of time (at a time), disabling all else until the second click, subtracting
        # the two and storing the total time for later subtraction from the total logging time.
        # All of the pause times are processed in the PauseCalc() class "pc".
        if request.form.get('pauseTime', '') == 'Pause' or request.form.get('pauseTime', '') == 'UnPause':
            if furnace.getPauseCount() == 0:
                # FIXME - Check if time since epoch UTC same for Win/Mac
                # grab time in seconds since epoch UTC
                tm = time.time()
                furnace.addPauseTime(tm)
                flash('Logging has been Paused at: ' + parseTime(str(time.ctime(tm))), 'warning')
                session['pauseBtnClicked'] = True
                furnace.writeToLog("Pause button clicked.") # TODO - hardcoded, remove!
            elif furnace.getPauseCount() == 1:
                tm = time.time()
                furnace.addPauseTime(tm)
                flash('Logging has been UnPaused at: ' + parseTime(str(time.ctime(tm))), 'warning')
                session['pauseBtnClicked'] = False
                furnace.writeToLog("UnPause button clicked.") # TODO - hardcoded, remove!
            return redirect(url_for('home'))

        # TODO - endTime grabs the last timestamp in the equation to decide total time for the calculation of total labels
        elif request.form.get('endTime', '') == 'Stop':
            tm = time.time()
            flash('All logging and counts have stopped at: ' +
                  parseTime(str(time.ctime(tm))), 'danger')
            session['startBtnClicked'] = False
            furnace.writeToLog("Stop button clicked.")
            # TODO - redirect to a final summation page
            return redirect(url_for('endofshift'))

        # TODO - enter the information for a new model for a mold change or print change
        # then updates the DB and present the last label count for the prior model
        # merely by selecting mold change from mouse pop up menu
        
        # jumps to settings page
        elif request.form.get('settings', '') == 'Settings':
            return redirect(url_for('settings'))

        # jumps to developer log page - soon to be depricated
        elif request.form.get('log', '') == 'Dev_Log':
            flash('This log is for development purposes only and will be removed from regular user interface in the future!', 'danger')
            return redirect(url_for('log'))

        # TODO - should this be here??  Pretty sure this is a whole 'nother world
        elif request.form.get('print', '') == 'Print':
            flash('Print button is working', 'success')
            furnace.writeToLog("Print button clicked.") # TODO - hardcoded, remove!
            return redirect(url_for('home'))
        elif request.form.get('glass', '') == 'Add Glass':
            return redirect(url_for('glass'))
            
    # If not post then get
    return render_template('home.html', title='Furnace Log', form=form)





# login to account
@ app.route('/login', methods=['GET', 'POST'])
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
            furnace.setFurnaceShift(3) # TODO - hard coded, remove!
            furnace.writeToLog("Logged in.")
            # TODO - write js to fade out alert
            flash('You are now logged in!', 'success')
            return redirect(url_for('start'))
        elif not existing_user:
            flash('Error with your username!', 'danger')
            return redirect(url_for('login'))
        else:
            flash('Password is incorrect', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Login!', form=form)



# index route .
@ app.route('/')
def index():
    return redirect(url_for('login'))



# log route - to view the class log file
@app.route('/log')
def log():
    form = furnace.getFurnaceLog()
    return render_template('log.html', form=form)



# settings route to input and change furnace info
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    username = session['username']
    existing_user = User.query.filter_by(username=username).first()
    form = SettingsForm(request.form)
    print(existing_user)
    if request.method == 'POST' and form.validate():
        wagonCount = request.form['wagonCount']
        furnaceNum = request.form['furnaceNum']
        speed = request.form['speed']

        existing_user.wagonCount = wagonCount
        existing_user.furnaceNum = furnaceNum
        existing_user.furnaceSpeed = speed
        db.session.commit()

        furnace.setWagonCount(wagonCount)
        furnace.setFurnaceNum(furnaceNum)
        furnace.setFurnaceSpeed(speed)
        return redirect(url_for('home'))
    return render_template('settings.html', form=form)



# add glass to db route
@app.route('/glass', methods=['GET', 'POST'])
def glass():
    form = GlassForm(request.form)
    if request.method == 'POST':
        modelnum = request.form['modelNum']
        jobnum = request.form['jobNum']
        adasnums = request.form['adas']
        measurenums = request.form['measure']
        existing_glass = Glass.query.filter_by(glassNum=modelnum).first()
        if existing_glass == modelnum:
            flash('Glass model ' + existing_glass + ' already exists!', 'danger')
            return redirect(url_for('glass'))
        if adasnums == None:
            glass = Glass(modelnum, jobnum, None, measurenums)
        else:
            glass = Glass(modelnum, jobnum, adasnums, measurenums)
        db.session.add(glass)
        db.session.commit()
        flash('New model ' + modelnum + ' added to the database!', 'success')
        return redirect(url_for('home'))
    return render_template('glass.html', title='Add Glass', form=form)



# end of shift landing page
@app.route('/endofshift')
def endofshift():
    return render_template('endofshift.html')



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
        furnaceNum = request.form['furnaceNumber']
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
                password), furnaceNum, loadingSide)
            db.session.add(new_user)
            db.session.commit()
            # FIXME - what needs to go and what needs to stay? login_required uses some of these
            session['username'] = new_user.username
            session['logged_in'] = True
            session['startBtnClicked'] = False
            session['pauseBtnClicked'] = False
            session['furnaceNumber'] = new_user.furnaceNum
            # FIXME - what needs to go and what needs to stay? some functionality currently uses 
            # some of these vs session[vars]
            furnace.furnaceNum(new_user.furnaceNum)
            furnace.setLoadSideOrNot(new_user.loadingSide)
            furnace.writeToLog("User created & logged in.")
            return redirect(url_for('home'))
        elif len(existing_user) > 0:
            flash('That username is already in use, try again!', 'danger')
            return redirect(url_for('setup'))
    else:
        return render_template('setup.html', title='Setup User', form=form)



# logout user
@ app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    session['frontOrBack'] = None
    furnace.writeToLog("Logged out.") 
    furnace.__del__()
    # FIXME - message does not fade out after logging out
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))



# requirements to be met before pages can be viewed
@app.before_request
def require_login():
    allowed_routes = ['login']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


# <<<-------------------------------------------------------->>>
if __name__ == '__main__':
    # global instance of Furnace class, right?
    furnace = Furnace()
    furnace.setFurnaceLogging()
    # spin 'er up!
    app.run(debug=True)
