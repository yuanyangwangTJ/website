import os
import datetime
from flask import Flask, Blueprint, url_for, render_template, request, make_response, redirect, abort, session, flash, g

from app.auth import login_required
from app.database import db, User, Activity, UPLOAD_FOLDER


bp = Blueprint('space', __name__)

@bp.route('/student/', methods=['GET', 'POST'])
@login_required
def personal_page():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return render_template('user.html', user_id=None, profile_image_path=None, user=None)

    if not (user.profile_image_path and user.profile_image_name):
        profile_image_path = None
    else:
        profile_image_path = os.path.join(
        user.profile_image_path, user.profile_image_name)

    return render_template('user.html', user_id=user_id, profile_image_path=profile_image_path, user=user)


# TO-DO need to build socre display part according to the pattern in user.html

