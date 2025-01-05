from shop import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile  = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')

    def __repr_(self):
        return '<User %r>' %self.username
    
        