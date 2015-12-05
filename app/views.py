from flask import render_template, flash, redirect, url_for, session, request
from app import app, db
from flask import render_template, flash, redirect, url_for, session, request, abort
from app import app, db, login_manager
from .forms import LoginForm, RegistrationForm
from .models import User, Meal, followers
from flask.ext.login import login_user, logout_user, login_required

#HOME
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.get(1) #marina
    user2 = User.query.get(2)
    #list of dictionaries
    meals = user.followed_posts().all()
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=meals)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']
        email = request.form['txtEmail']

        #user = User.query(filter_by=username)
        user = User.query.filter_by(username=username)
        if user.count() == 0:
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()

            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('login'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('register'))
    else:
        abort(405)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if request.method == 'GET':
            return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 1:
            login_user(user.one())
            flash('Welcome back {0}'.format(username))
            try:
                next = request.form['next']
                return redirect(next)
            except:
                return redirect(url_for('index'))
        else:
            flash('Invalid login')
            return redirect(url_for('login'))
    else:
        return abort(405)

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
