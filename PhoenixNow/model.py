from flask_sqlalchemy import SQLAlchemy
import os
import bcrypt
import datetime

db = SQLAlchemy()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    grade = db.Column(db.Integer)
    pw_hash = db.Column(db.String(500))
    salt = db.Column(db.String(100))
    checkedin = db.Column(db.Boolean)
    creation_timestamp = db.Column(db.DateTime)
    checkins = db.relationship('Checkin', backref='user', lazy='dynamic')
    verified = db.Column(db.Boolean)
    email_reminder = db.Column(db.String(50))
    email_reminder_id = db.Column(db.String(500))
    schedule_verified = db.Column(db.Boolean)
    schedule = db.Column(db.String(500))
    schedule_monday = db.Column(db.Boolean)
    schedule_tuesday = db.Column(db.Boolean)
    schedule_wednesday = db.Column(db.Boolean)
    schedule_thursday = db.Column(db.Boolean)
    schedule_friday = db.Column(db.Boolean)
    monday = db.Column(db.String(500))
    tuesday = db.Column(db.String(500))
    wednesday = db.Column(db.String(500))
    thursday = db.Column(db.String(500))
    friday = db.Column(db.String(500))
    profile_monday = db.Column(db.String(1000))
    profile_tuesday = db.Column(db.String(1000))
    profile_wednesday = db.Column(db.String(1000))
    profile_thursday = db.Column(db.String(1000))
    profile_friday = db.Column(db.String(1000))
    gcm_endpoint = db.Column(db.String(1000))
    followed = db.relationship('User', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')

    def __init__(self, firstname, lastname, grade, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.grade = grade
        self.pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.creation_timestamp = datetime.datetime.utcnow()
        self.checkedin = False
        self.verified = False
        self.schedule_verified = True
        self.schedule = "M:T:W:R:F"
        self.schedule_monday = True
        self.schedule_tuesday = True
        self.schedule_wednesday = True
        self.schedule_thursday = True
        self.schedule_friday = True
        self.monday = ""
        self.email_reminder = ""
        self.tuesday = ""
        self.wednesday = ""
        self.thursday = ""
        self.friday = ""
        self.profile_monday = ""
        self.profile_tuesday = ""
        self.profile_wednesday = ""
        self.profile_thursday = ""
        self.profile_friday = ""
	

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def is_authenticated(self):
        """Return True if the user is verified."""
        return self.verified

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.pw_hash.encode('utf-8'))

    def is_admin(self):
        if self.email in ['chaudhryam@guilford.edu', 'daynb@guilford.edu', 'admin@phoenixnow.me', 'kiddlm@guilford.edu', 'websternb@guilford.edu', 'lkiser@guilford.edu']:
          return True
        else:
          return False

    def is_super_admin(self):
        if self.email in ['kiddlm@guilford.edu', 'lkiser@guilford.edu']:
          return True
        else:
          return False

    def __repr__(self):
        return repr((self.lastname))

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_timestamp = db.Column(db.DateTime)
    checkin_week = db.Column(db.String(500))
    checkin_day = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self):
      self.checkin_timestamp = datetime.datetime.today()
      self.checkin_week = datetime.date.today().isocalendar()[1]
      self.checkin_day = datetime.date.today().isocalendar()[2]

    def __repr__(self):
        return "<Checkin(id='%s')>" % (self.id)

