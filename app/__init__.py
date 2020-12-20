import os

from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import and_
from . import auth, image, config, activity, space, module
from app.database import db, User, Activity

TEMPLATE_FOLDER = '../templates'
STATIC_FOLDER = '../static'
UPLOAD_FOLDER = '../upload'


# 应用工厂 可注册蓝图
def create_app(app_config=None):
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)
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

    # 五大模块蓝图
    app.register_blueprint(module.bp)

    @app.route("/")
    @app.route("/index")  # 主页
    @app.route("/index.html")
    @app.route("/home")
    def home():
        act1 = None
        act2 = None
        act3 = None
        try:
            user = User.query.filter(User.id == g.userid).first()
        except BaseException:
            return render_template('index.html', item1=act1, item2=act2, item3=act3)

        if user.usertype != 'student':
            return render_template('index.html', item1=act1, item2=act2, item3=act3)

        scores = {'virtue': 0, 'wisdom': 0, 'body': 0, 'beauty': 0, 'labor': 0}
        for activity in user.activities:
            if activity.status == 'finished' and activity.label in scores:
                scores[activity.label] += activity.score

        type_min = "virtue"
        num_min = scores["virtue"]
        for x, y in scores.items():
            if y < num_min:
                type_min = x

        recommend_act = db.session.execute('select * from activity where id in (select id from activity where status = "coming" and id not in(select Activity_id from tags where User_id = ' + str(user.id) + ')) limit 3;')
        recommend = []
        for activity in recommend_act:
            recommend.append(activity)

        length = len(recommend)
        for i in range(3 - length):
            recommend.append(None)

        return render_template('index.html', item1=recommend[0], item2=recommend[1], item3=recommend[2])

    return app
