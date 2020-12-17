from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

TEMPLATE_FOLDER = '../templates'
STATIC_FOLDER = '../static'
UPLOAD_FOLDER = '../upload'

# TO-DO add the database detail column
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    usertype = db.Column(db.Enum('student', 'teacher'),
                     nullable=False, default='student')
    password = db.Column(db.Text, nullable=False)
    profile_image_path = db.Column(db.String(255))
    profile_image_name = db.Column(db.String(255))

class Activity(db.Model):
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    discribe = db.Column(db.String(255))
    cover_image_path = db.Column(db.String(255))
    cover_image_name = db.Column(db.String(255))
    label = db.Column(db.Enum('virtue', 'wisdom', 'body',
                              'beauty', 'labor'), nullable=False)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    leed_teacher = db.Column(db.String(255), nullable=False)
    cover_path = db.Column(db.Text)
    max_join = db.Column(db.Integer)



class Apply(db.Model):
    __tablename__ = 'Apply'
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    userid = db.Column(db.Integer, nullable=False)
    actid = db.Column(db.Integer, nullable=False)
    #status = (db.Enum('apply', 'access'), nullable=False)
