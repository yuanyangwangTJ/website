import os

from flask import Flask, render_template

from . import db, auth, blog

def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=True,
                template_folder='../templates', static_folder='../static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )
    # 数据库示例 sqlite 需经讨论决定
    if app_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(app_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # 错误处理待定
        pass

    
    # 数据库初始化
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(auth.bp)

    # 博客蓝图
    app.register_blueprint(blog)

    @app.route('/', endpoint='index')
    def index():
        return render_template('index.html')

    return app
