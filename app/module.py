import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.database import db, User, Activity


def set_last_class_filter(index):
    if index % 2 == 0:
        return "last"
    else:
        return ""


bp = Blueprint('module', __name__)

bp.add_app_template_filter(set_last_class_filter, "set_last_class_filter")

@bp.route('/virtue', methods=['GET', 'POST'])
def virtue():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'virtue').all()
        return render_template('Virtue.html', item=act)
        

@bp.route('/wisdom', methods=['GET', 'POST'])
def wisdom():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'wisdom').all()
        return render_template('Wisdom.html', item=act)

@bp.route('/body', methods=['GET', 'POST'])
def body_act():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'body').all()
        return render_template('Body.html', item=act)


@bp.route('/beauty', methods=['GET', 'POST'])
def beauty():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'beauty').all()
        return render_template('Beauty.html', item=act)


@bp.route('/labor', methods=['GET', 'POST'])
def labor():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'labor').all()
        return render_template('Labor.html', item=act)

