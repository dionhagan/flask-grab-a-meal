from app import db
from flask import render_template, flash, redirect, url_for, session, request, abort
from app import db, login_manager
from app.models import User, Meal, followers
from flask.ext.login import login_user, logout_user, login_required, current_user
import datetime
from datetime import date
from app.main import main

''' 
    Util Functions
'''

# clean timestamps
def parse_timestamp(time):
    if time:
        time = str(time)[0:16]
        return time
    return '"Before Timestamp Implementation"'

# get user object from db
def get_user(search, url='/'):
    usr = User.query.filter_by(username=search)
    results = usr.all()
    if len(results) == 1:
        usr = usr.one()
        return usr
    else:
        flash('No user found with username "%s"' % search)
        return redirect(url_for('main.' + url))

# get most visited house location    
def most_visited(usr):
    from collections import defaultdict
    meals = defaultdict(int)
    posts = usr.meals
    if posts.count() > 1:
        for meal in posts:
            meals[meal.house] += 1
        return max(meals, key=meals.get)
    return 'None'
    
'''
    URL Routing
'''

#HOME
@main.route('/')
@main.route('/index')
@login_required
def index():
    #list of dictionaries
    meals = current_user.followed_posts().order_by(Meal.timestamp)
    for meal in meals:
        meal.date = parse_timestamp(meal.timestamp)
    return render_template('index.html',
                           title='Home',
                           meals=meals)

@main.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('main.login'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('main.register'))
    else:
        abort(405)

@main.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('main.index'))
        else:
            flash('Invalid login')
            return redirect(url_for('main.login'))
    else:
        return abort(405)

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/plan', methods=['GET', 'POST'])
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
        meal = Meal(house=house, time=time, author=current_user, timestamp=datetime.datetime.now())
        db.session.add(meal)
        db.session.commit()
        flash('Thank you for submitting your meal!')
        return redirect(url_for('main.index'))
    else:
        return abort(405)

@main.route('/house', methods=['GET', 'POST'])
@login_required
def house():
    if request.method == 'GET':
        locations = ['Adams', 'Annenberg', 'Cabot', 'Currier', 'Dunster', 'Eliot', 'Fly-By',
                    'Hillel', 'Kirkland', 'Leverett', 'Lowell', 'Mather', 'Pforzheimer',
                    'Quincy', 'Winthrop']
        return render_template("house.html", locations=locations)
    elif request.method == 'POST':
        location = request.form["location"]
        meals = []
        posts = current_user.followed_posts().order_by(Meal.timestamp)
        for meal in posts:
            if meal.house == location:
                meal.date = parse_timestamp(meal.timestamp)
                meals.append(meal)
        if len(meals) > 0:
            return redirect('/house-feed/%s' % location)
        else:
            flash('No meals found for %s' % location)
            return redirect(url_for('main.house'))
    else:
        abort(405)
        
@main.route('/house-feed/<loc>', methods=['GET'])
@login_required
def house_feed(loc):
    if request.method == 'GET':
        meals = []
        posts = current_user.followed_posts().order_by(Meal.timestamp)
        for meal in posts:
            if meal.house == loc:
                meal.date = parse_timestamp(meal.timestamp)
                meals.append(meal)
        return render_template("houseFriends.html", location=loc, meals=meals)
    else:
        abort(405)


@main.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    if request.method == 'GET':
        return render_template("find.html")
    elif request.method == 'POST':
        search = request.form['txtSearch']
        usr = User.query.filter_by(username=search)
        results = usr.all()
        if len(results) == 1:
            usr = usr.one()
            f = [str(u.username) for u in usr.followers.all()]
            if search in f:
                flash('Already following %s' % search)
                return redirect(url_for('main.index'))
            elif search == str(current_user.username):
                flash('Users cannot follow themselves')
                return redirect(url_for('main.index'))
            else:
                current_user.unfollow(usr)
                new_follower = current_user.follow(usr)
                db.session.add(new_follower)
                db.session.commit()
                flash('You are now following %s' % search)
                return redirect(url_for('main.index'))
        else:
            flash('No user found with username "%s"' % search)
            return render_template("find.html")
    else:
        abort(405)

@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/friends/<username>', methods=['GET'])
@login_required
def friends(username):
    if request.method == 'GET':
        # current user's own list of friends
        if username == current_user.username:
            friends = current_user.followed.all()
            if friends:
                return render_template("friends.html", friends=friends, user=current_user)
            else:
                print 'You are not following any other users'
        # user's friend's list of friends
        else:
            usr = get_user(username)
            friends = usr.followed.all()
            if friends:
                return render_template("friends.html", friends=friends, user=usr)
            else:
                flash('%s is not following any users' % usr.username)
                return redirect("/profile/%s" % username)
    else:
        abort(405)
        
@main.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    if request.method == 'GET':
        usr = get_user(username)
        friends = usr.followed.all()
        return render_template("profile.html", user=usr, nfriends=len(friends), most_vis=most_visited(usr))
    else:
        abort(405)