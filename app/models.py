from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    meals = db.relationship('Meal', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.name)

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	house = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime)
	meal_time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<House: %r, Time: %r>' % (self.house, self.meal_time)