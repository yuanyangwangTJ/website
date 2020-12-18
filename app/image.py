import time
import os
import datetime
import random

from werkzeug.utils import secure_filename
from flask import Flask, Blueprint, render_template, request, url_for, make_response, send_from_directory, abort, session, flash, g
import strutil
import base64

from app.auth import login_required
from app.database import db, User, Activity


class Pic_str:
    @staticmethod
    def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其䶿0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


bp = Blueprint('image', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['GET','POST'])
def profile_image_upload():
    if (request.method == 'GET'):
        return render_template('pages/profile.html')
    else:
        # get essential data
        f = request.files['image']
        user_id = session['user_id']

        # create the image saving path
        file_dir = os.path.join('upload','profile')
        user_path = os.path.join(file_dir, str(user_id))
        
        if not os.path.exists(user_path):
            os.makedirs(user_path)

        
        if f and allowed_file(f.filename):
            # securitify the filename
            fname = secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]
            new_filename = Pic_str.create_uuid() + '.' + ext
            f.save(os.path.join(user_path, new_filename))

            # update profile image path the database
            user = User.query.filter(User.id == user_id).first()
            user.profile_image_path = user_path
            user.profile_image_name = new_filename
            db.session.commit()
            # complete feedback
            flash('Upload succeeded!')
            # TO-DO redact the url to prevent from 404 
            return render_template(url_for("space.personal_page"))
        else:
            flash('The image format is not supported. Please try again.')
            render_template('pages/profile.html')



# display different users profile image in comments etc.
# return the relative path of the image
def profile_image_directory(user_id):
    user = User.query.fliter(User.id == user_id)
    if user is None:
        return None
    else:
        # TO-DO edit the iamge path for frontend to find the image
        return os.path.join('../../website',user.profile_image_directory, user.profile_image_name)


# TO-DO rewrite the function
# download the image of request
@bp.route('/download/<string:filename>/', methods=['GET'])
# need to login before download any image
@login_required
def image_download():
    if request.method == 'GET':
        file_path = os.path.join('upload', 'profile')
        user_id = session['user_id']
        
        filename = g.user.profile_image_name
        if os.path.isfile(file_path, filename):
            return send_from_directory(file_path, filename, as_attachment=True)


# show photo
# TO-DO: file path need to change
@bp.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, 'upload')
    if request.method == 'GET':
        if filename is None:
            return render_template('404.html')
        else:
            image_data = open(os.path.join(file_dir, '%s' %
                                           filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

