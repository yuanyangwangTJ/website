import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db, User, Activity

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/regist/', methods=('GET', 'POST'))
def regist():
    if (request.method == 'GET'):
        return render_template("auth/regist.html")
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if (userid == ''):
            return render_template("auth/regist.html", text="请填入学号")
        if (password == ''):
            return render_template("auth/regist.html", text="请填入密码")

        user = User.query.filter(User.id == userid).first()
        if (user):
            return render_template("auth/regist.html", text="该学号已经注册")
        elif (password != password2):
            return render_template("auth/regist.html", text="两次密码不同，请核对")
        else:
            user = User(id=userid, type='normal',password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

    return redirect(url_for("auth.login"))


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if (request.method == 'GET'):
        return render_template("auth/login.html")
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        user = User.query.filter(User.id == userid).first()

        if (user == None):
            return render_template("auth/login.html", text="请先注册")
        if (user.password != check_password_hash(password)):
            return render_template("auth/login.html", text="密码错误")
        session['userid'] = user.id
        session['usertype'] = user.type

    return redirect(url_for('home'))


@bp.route('/logout/')
def logout():
    session.pop('userid')
    session.pop('usertype')
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
