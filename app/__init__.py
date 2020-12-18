import os

from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for

from . import auth, image, config, activity, space
from app.database import db, Activity, User


TEMPLATE_FOLDER = '../templates'
STATIC_FOLDER = '../static'
UPLOAD_FOLDER = '../upload'

# 应用工厂 可注册蓝图
def create_app(app_config=None):
    app = Flask(__name__, template_folder= TEMPLATE_FOLDER,
                static_folder= STATIC_FOLDER)
    app.config.from_object(config)
    app.config['UPLOAD_FOLFER'] = UPLOAD_FOLDER
    
    # 数据库初始化
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    
    # 注册蓝图
    app.register_blueprint(auth.bp)

    # 图片操作蓝图
    app.register_blueprint(image.bp)

    # 活动页蓝图
    app.register_blueprint(activity.bp)

    # 个人主页蓝图
    app.register_blueprint(space.bp)

    @app.route("/")
    @app.route("/index")  # 主页
    @app.route("/index.html")
    @app.route("/home")
    def home():
        Acts = []
        Acts = Activity.query.order_by(Activity.id.desc()).all()
        args = {
            'session': session,
            'acts': Acts
        }
        return render_template('index.html')


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
