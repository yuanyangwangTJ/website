import os
import datetime
from flask import Flask, Blueprint, url_for, render_template, request, make_response, redirect, abort, session, flash, g
from flask_sqlalchemy import SQLAlchemy

from app.auth import login_required
from app.database import db, User, Activity, UPLOAD_FOLDER

def stat_scores(student):
    """
    count virtue score
    :param student: student, a User instance
    :return: dict: total scores, None means student don't exist
    """
    if student.usertype != 'student':
        return None

    scores = {'virtue': 0, 'wisdom': 0, 'body': 0, 'beauty': 0, 'labor': 0}
    for activity in student.activities:
        if activity.status == 'finished' and activity.label in scores:
            scores[activity.label] += activity.score

    return scores


bp = Blueprint('space', __name__)

@bp.route('/student/', methods=['GET', 'POST'])
@login_required
def personal_page():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return render_template('./pages/user.html', user_id=None, profile_image_path=None, user=None, scores={'virtue': 0, 'wisdom': 0, 'body': 0, 'beauty': 0, 'labor': 0})

    if not (user.profile_image_path and user.profile_image_name):
        profile_image_path = None
    else:
        profile_image_path = os.path.join(
        user.profile_image_path, user.profile_image_name)

    scores = stat_scores(user)
    total_score = scores['virtue'] + scores['wisdom'] + scores['body'] + scores['beauty'] + scores['labor']
    return render_template('./pages/user.html', user_id=user_id, profile_image_path=profile_image_path, user=user, scores=scores, total_score=total_score)


# TO-DO need to build socre display part according to the pattern in user.html

