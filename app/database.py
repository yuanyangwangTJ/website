from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.Enum('normal', 'admin'),
                     nullable=False, default='normal')
    password = db.Column(db.String(255))


class Activity(db.Model):
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    text = db.Column(db.Text)


class Apply(db.Model):
    __tablename__ = 'Apply'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    userid = db.Column(db.Integer, nullable=False)
    actid = db.Column(db.Integer, nullable=False)
    #status = (db.Enum('apply', 'access'), nullable=False)
