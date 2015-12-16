from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
	)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    meals = db.relationship('Meal', backref='author', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count()

    def followed_posts(self):
        return Meal.query.join(followers, (followers.c.followed_id == Meal.user_id)).filter(followers.c.follower_id == self.id).order_by(Meal.timestamp.desc())

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(128))
	meals = db.relationship('Meal', backref='author', lazy='dynamic')
	authenticated = db.Column(db.Boolean, default=False)
	followed = db.relationship('User', 
							   secondary=followers, 
							   primaryjoin=(followers.c.follower_id == id), 
							   secondaryjoin=(followers.c.followed_id == id), 
							   backref=db.backref('followers', lazy='dynamic'), 
							   lazy='dynamic')

	def __repr__(self):
		return '<User %r>' % (self.username)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count()

	def followed_posts(self):
		return Meal.query.join(followers, (followers.c.followed_id == Meal.user_id)).filter(followers.c.follower_id == self.id).order_by(Meal.timestamp.desc())

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	house = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime)
	meal_time = db.Column(db.DateTime)
	time = db.Column(db.String(12))
	date = db.Column(db.String(16))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<House: %r, Time: %r>' % (self.house, self.time)
