import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db, User, Activity

bp = Blueprint('auth', __name__)

@bp.route('/regist', methods=['GET', 'POST'])
def regist():
    if (request.method == 'GET'):
        return render_template("signup.html")
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        identity = request.form.get('identity')

        if (userid == ''):
            return render_template("signup.html", text="请填入学号")
        if (password == ''):
            return render_template("signup.html", text="请填入密码")

        user = User.query.filter(User.id == userid).first()
        if (user):
            return render_template("signup.html", text="该用户已经注册")
        elif (password != password2):
            return render_template("signup.html", text="两次密码不同，请核对")
        else:
            user = User(id=userid, usertype=identity, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

    return redirect(url_for("auth.login"))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        userid = request.form.get('userid')
        password_input = request.form.get('password')
        user = User.query.filter(User.id == userid).first()

        if user == None:
            return render_template("login.html", text="请先注册")
        if not check_password_hash(user.password, password_input):
            return render_template("login.html", text="密码错误")
        
    session['user_id'] = user.id
    session['usertype'] = user.usertype
    return redirect(url_for("space.personal_page",id=userid))


@bp.before_app_request
def load_logged_in_user():
    try:
        user_id = session['user_id']
        user_type = session['usertype']
    except:
        user_id = None
        user_type = None

    if user_id is None:
        g.user = None
        g.usertype = None
    else:
        g.user = User.query.filter(User.id == user_id)
        g.usertype = user_type
        g.userid = user_id


@bp.route('/logout',methods=['GET','POST'])
def logout():
    try:
        session.pop('user_id')
        session.pop('usertype')
    except:
        pass
    g.user = None
    g.usertype = None
    g.userid = None
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('You need to login first.')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
