from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.database import db, User, Activity

bp = Blueprint('act', __name__)

# TO-DO complete the activity info transfer to database
# fill in the blank like 'src=' or 'href'

@bp.route('/new', methods=['POST', 'GET'])  # 新建活动
def new():
    if (session['usertype'] != 'admin'):
        return redirect(url_for('home'))

    if (request.method == 'GET'):
        return render_template("new.html")
    else:
        actname = request.form.get('actname')
        context = request.form.get('context')
        if (actname == ""):
            return render_template("new.html", text="请填入活动名称")
        acti = Activity(name=actname, text=context)
        db.session.add(acti)
        db.session.commit()

    return redirect(url_for('new'))


@bp.route('/<int:id>/', methods=['POST', 'GET'])
def activity(id):
    act = Activity.query.filter(Activity.id == id).first()
    if (request.method == 'POST'):
        if (session['usertype'] != 'student'):#teacher和admin可以删除活动
            act.delete()
            db.session.commit()
            return redirect(url_for("home"))
        elif (session['usertype'] == 'student'):#studendt可以报名
            student = User.query.filter(User.id == g.userid).first()#取当前用户的id？
            if (student not in act.participants):#判断正确性存疑？
                activity.participants.append(student)
                db.session.commit()
    if (act == None):
        return redirect(url_for("home"))
    args = {
        'session': session,
        'act': act
        }
    return render_template("activity-demo.html", **args, activity=act)
