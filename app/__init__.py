import os

from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for

from . import auth, blog, config, activity
from app.database import db, Activity, User

# 应用工厂 可注册蓝图
def create_app(app_config=None):
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config)
    
    # 数据库初始化
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    
    # 注册蓝图
    app.register_blueprint(auth.bp)

    # 博客蓝图
    # app.register_blueprint(blog.bp)

    # 活动页蓝图
    app.register_blueprint(activity.bp)


    @app.route("/")  # 主页
    def home():
        Acts = []
        Acts = Activity.query.order_by(Activity.id.desc()).all()
        args = {
            'session': session,
            'acts': Acts
        }
        return render_template("index.html", **args)


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
