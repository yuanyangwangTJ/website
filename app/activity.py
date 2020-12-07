from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.database import db, User, Activity, Apply

bp = Blueprint('act', __name__, url_prefix='/act')

@bp.route('/new/', methods=['POST', 'GET'])  # 新建活动
def new():
    if (session['usertype'] != 'admin'):
        return redirect(url_for('home'))

    if (request.method == 'GET'):
        return render_template("act/new.html")
    else:
        actname = request.form.get('actname')
        context = request.form.get('context')
        if (actname == ""):
            return render_template("act/new.html", text="请填入活动名称")
        acti = Activity(name=actname, text=context)
        db.session.add(acti)
        db.session.commit()

    return redirect(url_for('act.new'))


@bp.route('/<int:id>/', methods=['POST', 'GET'])
def activity(id):
    if (request.method == 'POST'):
        if (session['usertype'] == 'admin'):
            Activity.query.filter(Activity.id == id).delete()
            Apply.query.filter(Apply.actid == id).delete()
            db.session.commit()
        elif (session['usertype'] == 'normal'):
            apply = Apply.query.filter(
                Apply.actid == id and Apply.userid == session['userid']).first()
            if (apply == None):
                apply = Apply(actid=id, userid=session['userid'])
                db.session.add(apply)
                db.session.commit()
    act = Activity.query.filter(Activity.id == id).first()
    if(act == None):
        return redirect(url_for("home"))
    args = {
        'session': session,
        'act': act
    }
    return render_template("act/activity.html", **args)
