from app import app, db
from flask import render_template, flash, redirect, url_for, session, request, abort
from app import app, db, login_manager
from .forms import LoginForm, RegistrationForm
from .models import User, Meal, followers
from flask.ext.login import login_user, logout_user, login_required, current_user
import datetime
from datetime import date

#HOME
@app.route('/')
@app.route('/index')
@login_required
def index():
    #list of dictionaries
    meals = current_user.followed_posts().all()
    return render_template('index.html',
                           title='Home',
                           meals=meals)

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
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 1:
            login_user(user.one())

            #current_user = user.one()
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

@app.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    if request.method == 'GET':
        houses = ['Adams', 'Annenberg', 'Cabot', 'Currier', 'Dunster', 'Eliot', 'Fly-By',
                    'Hillel', 'Kirkland', 'Leverett', 'Lowell', 'Mather', 'Pforzheimer',
                    'Quincy', 'Winthrop']
        times = ['7:30 AM', '7:45 AM', '8:00 AM', '8:15 AM', '8:30 AM', '8:45 AM', '9:00 AM',
                '9:15 AM', '9:30 AM', '9:45 AM', '10:00 AM', '11:30 AM', '11:45 AM', '12:00 PM', 
                '12:15 PM', '12:30 PM', '12:45 PM', '1:00 PM', '1:30 PM', '1:45 PM', '2:00 PM',
                '2:15 PM', '2:30 PM', '5:00 PM', '5:15 PM', '5:30 PM', '5:45 PM', '6:00 PM',
                '6:15 PM', '6:30 PM', '6:45 PM', '7:00 PM', '7:15 PM']
        return render_template('plan.html', houses=houses, times=times)
    elif request.method == 'POST':
        print 'posted'
        user_id = current_user.id
        house = request.form['house']
        time = request.form['time']
        meal = Meal(house=house, time=time, author=current_user)
        db.session.add(meal)
        db.session.commit()
        flash('Thank you for submitting your meal!')
        return redirect(url_for('index'))
    else:
        return abort(405)

@app.route('/house', methods=['GET', 'POST'])
def house():
    return redirect(url_for('index'))

@app.route('/find')
def find():
    if request.method == 'GET':
        all_users = []
        for usr in User.query.all():
            if usr.username != current_user.username:
                all_users.append(usr)
        return render_template("find.html", all_users = all_users)
    elif request.method == 'POST':
        pass
    else:
        abort(405)
    return redirect(url_for('index'))
