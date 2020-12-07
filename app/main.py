import config
from flask import Flask, request, render_template, redirect, url_for, g, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    type = db.Column(db.Enum('normal', 'admin'),nullable=False,default='normal')
    password = db.Column(db.String(255))

class Activity(db.Model):
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.String(256),nullable=False)
    text = db.Column(db.Text)

db.create_all()
Acts=[]

@app.route("/")  # 主页
def home():
    global Acts
    Acts=Activity.query.order_by(Activity.id.desc()).all()
    args = {
        'session': session,
        'acts':Acts
    }
    return render_template("index.html",**args)


@app.route('/login/', methods=['POST', 'GET'])  # 登录界面
def login():
    if (request.method == 'GET'):
        return render_template("login.html")
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        user = User.query.filter(User.id == userid).first()
        if (user==None):
            return render_template("login.html",text="请先注册")
        if (password != user.password):
            return render_template("login.html",text="密码错误")
        session['userid']=user.id
        session['usertype']=user.type
    return redirect(url_for('home'))

@app.route('/logout/')  # 注销
def logout():
   session.pop('userid')
   session.pop('usertype')
   return redirect(url_for('home'))

@app.route('/new/', methods=['POST', 'GET'])  # 新建活动
def new():
    if (session['usertype'] != 'admin'):
        return redirect(url_for('home'))
    
    if (request.method == 'GET'):
        return render_template("new.html")
    else:
        actname = request.form.get('actname')
        context = request.form.get('context')
        if (actname==""):
            return render_template("new.html", text="请填入活动名称")
        acti = Activity(name=actname, text=context)
        db.session.add(acti)
        db.session.commit()



    return redirect(url_for('new'))




@app.route('/regist/', methods=['POST', 'GET'])  # 注册界面
def regist():
    if (request.method == 'GET'):
        return render_template("regist.html")
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if (userid==''):
            return render_template("regist.html",text="请填入学号")
        if (password==''):
            return render_template("regist.html",text="请填入密码")

        user = User.query.filter(User.id == userid).first()
        if (user):
            return render_template("regist.html",text="该学号已经注册")
        elif (password != password2):
            return render_template("regist.html",text="两次密码不同，请核对")
        else:
            user = User(id=userid,type='normal', password=password)
            db.session.add(user)
            db.session.commit()
    return redirect(url_for("login"))

@app.route('/activity/<id>/', methods=['POST', 'GET'])
def activity(id):
    if (request.method == 'POST'):
        if (session['usertype'] == 'admin'):
            Activity.query.filter(Activity.id == id).delete()
            db.session.commit()
    act=Activity.query.filter(Activity.id == id).first()
    if(act==None):
        return redirect(url_for("home"))
    args = {
        'session': session,
        'act':act
    }
    return render_template("activity.html",**args)


if (__name__ == "__main__"):
    app.run()
