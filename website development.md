# 计算机科学导论网站设计

## 1. 网站设计动机

**德育课堂**是同济大学2019年在新生院开始实施的学生培养方案，旨在培养德智体美劳全面发展的同济大学生，政策也保留到了大二的电信学院。但是我们发现，目前电信学院并没有**官方的二课堂网站**，因此我们产生了利用此次网页作业制作一个德育课堂网站的想法，来实现德育活动的基本运行，也开始了网站的设计制作.

****

## 2. 网站功能

网站提供一个第二课堂活动运行的基本逻辑功能。学生教师可以注册不同的身份，进入不同的登录界面。教师端具有活动发布、活动修改、活动批准的基本功能；学生端可以查看教师发布的活动，进行报名申请，当然，根据实际逻辑，学生也可以取消活动，根据教师确认活动完成来获得相应的德育分数，更新到学生的主页部分。不仅如此，教师和学生页面也有相似的功能，具有个人页面的主题切换功能，具有头像的设定、修改与显示功能；首页具有智能推送内容，可以推送近期的德育活动；也有首页模块的展示功能等等.

简单的逻辑列举如下：

* **同学端：**1.活动报名/取消报名	2.查看各模块的分数
* **教师端：**1.发布/删除/修改活动	2.终止活动	
* **课堂网站：**	1.注册/登录/退出    2.活动展示以及详情查看

****

## 3. 分工

计算机科学导论第五小组具体分工如下：

* **前端：**王远洋，王嘉俊，王麒斌
* **后端：**裘自立，徐佳春，韩孟霖
* **前后端连接以及后端：**熊玮

****

## 4. 技术路线

网站的技术路线可以分为前后端来阐述，具体分析介绍如下：

### I. 前端技术路线

<img src="C:\Users\86152\AppData\Roaming\Typora\typora-user-images\image-20201223161134869.png" alt="image-20201223161134869" style="zoom: 80%;" />

****

### II. 后端技术路线

#### 1. `Flask`

##### 1.1 应用工厂

在起步阶段依据 [Flask 中文文档](https://dormousehole.readthedocs.io/en/latest/tutorial/factory.html ) 设置了应用工厂及`__init__.py`文件，这样操作方便了后续所有应用的相关配置的添加。同时当在服务器端部署网站时，利用`setup.py`可以直接将网站应用视为一个`python`包。

例如项目静态文件的目录：

```
TEMPLATE_FOLDER = '../templates'
STATIC_FOLDER = '../static'
```

应用工厂：

```python
def create_app(app_config=None):
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER,
                static_folder=STATIC_FOLDER)
    app.config.from_object(config)
    # ...
    return app
```

数据库初始化：

```python
db.init_app(app)
with app.test_request_context():
    db.create_all()
```

功能蓝图的注册：

```python
app.register_blueprint(auth.bp)
```

主页的路由：

```python
 @app.route("/home")
    def home():
    	# ...
    	return render_template('index.html')
```

##### 1.2 蓝图视图

项目充分利用了 `Flask`提供的**蓝图与视图**功能，蓝图可以组织一组相关功能，视图则可以对请求进行响应。

例如注册页的蓝图：

```python
bp = Blueprint('auth', __name__, pre_fix='auth')
```

视图的动态URL生成：

```python
@bp.route('/<int:id>/', methods=['POST', 'GET'])
def activity(id):
	# ...
	return ...
```

视图的装饰器：

```python
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('You need to login first.')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
```

##### 1.3 后端参数传递

利用`redirect()` `url_for()` `render_tamplete()`等函数进行参数传递，将需要的内容传递到前端以便展示：

```python
render_template('pages/user.html', user_id=None,
                 profile_image_path=None, user=None,
                 scores={'virtue': 0, 'wisdom': 0, 'body': 0, 'beauty': 0, 'labor': 0})
```

****

#### 2. `Jinja`

##### 2.1 Jinja 模板复用

`Jinja`提供了非常易用的模板复用功能：

```jinja2
{% extends 'base.html' %}
```

这样可以方便地复用基础模板，再加上`block`块的输出替换可以实现对`html`文档`head` `title` `content`等的轻松替换：

```jinja2
{% block title %}
	...
{% endblock title %}
```

##### 2.2 网页内容的动态控制

当用户请求后，后端数据库将查询到的内容动态返回到前端时，`Jinja`的控制语句能够很好地控制动态内容的显示：

```jinja2
{% for activity in item %}
        <li class="{{ loop.index0 | set_last_class_filter }}"><img 
        		src="{{activity.cover_image_path ~ activity.cover_image_name}}" alt="" />
            <h2>{{activity.name}}</h2>
            <p>{{activity.description}}</p>
            <p class="readmore"><a href="{{'../' ~ activity.id}}">Read More Here &raquo;</a></p>
        </li>
 		{% else %}
        <h2>No Activity.</h2>
{% endfor %}
```

****

#### 3. `Flask-SqlAlchemy`

##### 3.1 建立数据库模型

利用`Flask`支持的 ORM `Flask_SqlAlchemy`在`database.py`中建立网站运行后需要创建的数据库形式：

```python
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    usertype = db.Column(db.Enum('student', 'teacher', 'admin'),
                     nullable=False, default='student')
    password = db.Column(db.Text, nullable=False)
    # ...
```

##### 3.2 视图数据库查询

在视图处理函数内，可以通过`db`对象进行对数据库的多项操作，包括增删改查，多对多表的条件筛选等：

```python
# 查询
student = User.query.filter(User.id == g.userid).first()
# 删除参与人员
act = Activity.query.filter(Activity.id == activity_id).first()
student = User.query.filter(User.id == g.userid).first()
act.participants.remove(student)
db.session.commit()

```

****

## 5. 网站关键技术实现

网站的关键技术也是分前后端来论述：

****

### I. 前端关键技术实现

构建`Base.html`作为活动展示类页面的`jinja2`模板基础页面，包含搜索框、上端导航边栏、日历挂件、活动展示区、地图连接等部分。
在`Base.html`的基础上利用`jinja2`渲染的方式统一搭建德智体美劳五个板块的展示页、活动详情页等页面，保证风格一致。
登入登出页面设置统一的动态背景，设置下拉框选择用户身份，利用`JavaScript`完成账号信息交互的同时实现错误处理功能。
构建`base.html`作为用户操作类页面的`jinja2`模板基础页面，包含搜索框、左侧导航边栏、设置和消息通知以及退出登录的按钮组、时间展示模块等内容。与用户有关的信息展示利用`JavaScript`从后端数据库拉取。
在`base.html`的基础上利用`jinja2`渲染的方式统一搭建教师和学生的账户主页、活动发布活动修改等页面，保证风格一致。在个人主页中利用表格展示活动信息，教师端展示报名活动的学生信息，学生端展示自己的活动报名状态。
基于前端主流框架`Bootstrap`开发，各页面通过响应式`jQuery`设计获取用户在前端页面的操作信息。

****

### II.后端关键技术实现

#### 后端数据库

使用`SQLAlchemy`建立数据库。
首先建立两个类，`User`和`Activity`分别用于存放用户和活动的相关信息。
一个学生可能参加多个活动，同时，一个活动可能被多个学生参加，因此，`User`和`Activity`之间需要建立多对多的关系。表格`tags`用于记录这个多对多的关系，`tags`有两个外键，分别是`User.id`和`Activity.id`，具体如下：

```python
tags = db.Table('tags',
    db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('Activity_id', db.Integer, db.ForeignKey('Activity.id'))
)
```

给`Activity`类加一个`Activity.participants`属性，具体如下：

```python
participants = db.relationship('User', secondary=tags,
       backref=db.backref('activities', lazy='dynamic'))
```

`Activity.participants`可以通过活动找到报名参与活动的用户，而`User.activities`可以通过用户找到用户报名参与的活动。

****

## 6.网站效率以及安全性

优秀的网站除了良好的UI之外，也需要**网站数据安全**的保护，作为第二课堂网站，对于学生分数的保护，登录的限制，尤其需要数据保护，这些功能的实现更多是体现在后端的数据库实现。另外，网站还需要有执行效率的考虑，更多的，对于`Windows\Mac\Linux`三大主流系统的兼容性，以及数据库的并行安全等也在考虑的范围之内.

* **执行效率：**在部分需要复杂逻辑的地方，由于`Python`作为解释型语言，其执行效率不高，因此采用MySQL语句代替`Python`逻辑，加快数据的查询，例如学生首页的活动推荐。 `# __init__.py Line 67`

* **安全性：**使用`SHA256`处理用户的密码后再存储于数据库中以加强安全性。假使数据库被不法分子攻破，也能保证攻击者拿不到用户的密码明文，减少了用户密码泄露的可能性。

  采用`sql Alchemy`的默认特性，可以防止一般的`sql`注入攻击；在直接使用`SQL`语句的代码处，所有的变量都不由用户输入，同样不会被`sql`注入攻击。`# __init__.py Line 67`

* **多系统适配：**由于`Windows`采用`’\’`作为文件路径分隔符，而`macOS`和`Linux`采用’/‘作为文件路径分隔符，我们将多种系统分隔符统一为`’/‘`后再写入数据库中；而在读取路径以加载文件时，利用`Python`的特性可以直接加载读取。加之，这项特性也可以实现将网站部署到任意配置了环境的`Windows/Linux/macOS`服务器中而不需要修改代码。 `# ![img](file:///C:\Users\86152\AppData\Roaming\Tencent\QQ\Temp\%W@GJ$ACOF(TYDYECOKVDYB.png)activity.py Line 55 - 58`

* **并发安全：**将用户上传的文件以上传时间重命名，确保用户上传的文件名不会导致数据库紊乱。同时在重命名时加入随机数后缀，保证在同一时间单位内能够处理更多的文件上传。

  采用MySQL的线程安全特性，实现了对数据库的并发增删改查操作。

****

## 7. 代码

本网站为开源项目，可以在[**Github仓库**](https://github.com/yuanyangwangTJ/website.git)查看.

### 网站项目代码整理

- **后端**

  - [\_\_init\_\_.py](https://github.com/yuanyangwangTJ/website/blob/master/app/__init__.py)

    ```python
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
    ```
    
  - [activity.py](https://github.com/yuanyangwangTJ/website/blob/master/app/activity.py)

    ```python
    from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
    import os
    import datetime
    from app.database import db, User, Activity
    from app.image import basedir, allowed_file
    from werkzeug.utils import secure_filename
    
    
    bp = Blueprint('act', __name__)
    
    # fill in the blank like 'src=' or 'href'
    
    @bp.route('/new', methods=['POST', 'GET'])  # 新建活动
    def new():
        if session['usertype'] != 'admin' and session['usertype'] != 'teacher':
            return redirect(url_for('home'))
    
        if request.method == 'GET':
            
            return render_template("teacher/pubActivity.html")
        else:
            name = request.form.get('name')
            description = request.form.get('description')
            # cover_image_path = request.form.get('cover_image_path')
            cover_image_name = request.form.get('cover_image_name')
            label = request.form.get('label')
            lead_teacher = request.form.get('lead_teacher')
            score = request.form.get('score')
            # participants = request.form.get('participants')
            # upload image
            cover_image_path = os.path.join('.', 'static', 'img', 'activity')
    
            f = request.files['image']
    
            if name == "":
                flash('请填入活动名称')
                return render_template("teacher/pubActivity.html")
            if label == "":
                flash('请填入活动类型')
                return render_template("teacher/pubActivity.html")
            if lead_teacher == "":
                flash('请填入带队老师')
                return render_template("teacher/pubActivity.html")
    
            cover_image_name = ""
    
            if f and allowed_file(f.filename):
                # securitify the filename
                fname = secure_filename(f.filename)
                ext = fname.rsplit('.', 1)[1]
                nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
                cover_image_name = nowTime + '.' + ext
    
                cover_image_path += os.sep
                cover_image_path = cover_image_path.replace('\\', '/')
                path = os.path.abspath(os.path.join(cover_image_path, cover_image_name))
    
                f.save(path)
    
                # complete feedback
                flash('Upload succeeded!')
                # TO-DO redact the url to prevent from 404
            else:
                flash('The image format is not supported. Please try again.')
    
            acti = Activity(name=name, description=description, cover_image_path=cover_image_path,
                            cover_image_name=cover_image_name, label=label, lead_teacher=lead_teacher, score=score,
                           # participants=participants
                           )
    
            db.session.add(acti)
            db.session.commit()
    
        return redirect(url_for('act.activity', id=acti.id))
    
    @bp.route('/<int:id>/', methods=['POST', 'GET'])
    def activity(id):
        act = Activity.query.filter(Activity.id == id).first()
        args = {
            'session': session,
            'act': act
            }
        if act is None:
            return redirect(url_for("home"))
        if 'usertype' not in session:
            return render_template("activity-demo.html", **args, activity=act, isApplied='')
        # if (request.method == 'POST'):
        if session['usertype'] != 'student':#teacher和admin可以删除活动
            return render_template("activity-demo.html", **args, activity=act, operation='Delete')
        elif session['usertype'] == 'student':#studendt可以报名
            student = User.query.filter(User.id == g.userid).first()#取当前用户的id？
            if student not in act.participants:#判断正确性存疑？
                return render_template("activity-demo.html", **args, activity=act, operation='Apply')
            else:
                return render_template("activity-demo.html", **args, activity=act, operation='Abort')
        return render_template("activity-demo.html", **args, activity=act, isApplied='')
    
    @bp.route('/apply/<int:activity_id>')
    def apply(activity_id):
        act = Activity.query.filter(Activity.id == activity_id).first()
        student = User.query.filter(User.id == g.userid).first()
        act.participants.append(student)
        db.session.commit()
        return redirect(url_for('act.activity', id=activity_id))
    
    @bp.route('/abort/<int:activity_id>')
    def abort(activity_id):
        act = Activity.query.filter(Activity.id == activity_id).first()
        student = User.query.filter(User.id == g.userid).first()
        act.participants.remove(student)
        db.session.commit()
        return redirect(url_for('act.activity', id=activity_id))
    
    @bp.route('/delete/<int:activity_id>')
    def delete(activity_id):
        act = Activity.query.filter(Activity.id == activity_id).first()
        db.session.delete(act)
        db.session.commit()
        return redirect(url_for("home"))
    
    @bp.route('/complete/<int:activity_id>')
    def complete(activity_id):
        act = Activity.query.filter(Activity.id == activity_id).first()
        act.status = 'finished'
        db.session.commit()
        return redirect(url_for('act.activity', id=activity_id))
    
    @bp.route('/revise/<int:activity_id>', methods=['POST', 'GET'])
    def revise(activity_id):
        act = Activity.query.filter(Activity.id == activity_id).first()
        if act is None:
            return redirect(url_for("home"))
        if request.method == 'GET':
    
            return render_template("teacher/reviseActivity.html", activity_id=activity_id, act=act)
        else:
            name = request.form.get('name')
            description = request.form.get('description')
            # cover_image_path = request.form.get('cover_image_path')
            # cover_image_name = request.form.get('cover_image_name')
            label = request.form.get('label')
            lead_teacher = request.form.get('lead_teacher')
            score = request.form.get('score')
            # participants = request.form.get('participants')
            # upload image
            cover_image_path = os.path.join('.', 'static', 'img', 'activity')
    
            f = request.files['image']
    
            if name == "":
                flash('请填入活动名称')
                return render_template("teacher/reviseActivity.html", activity_id=activity_id, act=act)
            if label == "":
                flash('请填入活动类型')
                return render_template("teacher/reviseActivity.html", activity_id=activity_id, act=act)
            if lead_teacher == "":
                flash('请填入带队老师')
                return render_template("teacher/reviseActivity.html", activity_id=activity_id, act=act)
    
            cover_image_name = ""
    
            if f and allowed_file(f.filename):
                # securitify the filename
                fname = secure_filename(f.filename)
                ext = fname.rsplit('.', 1)[1]
                nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
                cover_image_name = nowTime + '.' + ext
    
                # path = os.path.abspath(os.path.join(cover_image_path, cover_image_name))
                # path = path.replace('\\', '/')
                cover_image_path += os.sep
                cover_image_path = cover_image_path.replace('\\', '/')
                path = os.path.abspath(os.path.join(cover_image_path, cover_image_name))
    
                f.save(path)
    
                # complete feedback
                flash('Upload succeeded!')
                # TO-DO redact the url to prevent from 404
            else:
                flash('The image format is not supported. Please try again.')
    
    
            act.name = name
            act.description = description
            act.cover_image_path = cover_image_path
            act.cover_image_name = cover_image_name
            act.label = label
            act.lead_teacher = lead_teacher
            act.score = score
            db.session.commit()
    
        return redirect(url_for('act.activity', id=activity_id))
    
    ```
    

- [auth.py](https://github.com/yuanyangwangTJ/website/blob/master/app/auth.py)
  
  ```python
    import functools
    
    from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
    
    from werkzeug.security import check_password_hash, generate_password_hash
    from app.database import db, User, Activity
    
    bp = Blueprint('auth', __name__)
    
    @bp.route('/regist', methods=['GET', 'POST'])
    def regist():
        if (request.method == 'GET'):
            return render_template("signup.html")
        else:
            userid = request.form.get('userid')
            password = request.form.get('password')
            password2 = request.form.get('password2')
            identity = request.form.get('identity')
    
            if (userid == ''):
                return render_template("signup.html", text="请填入学号")
            if (password == ''):
                return render_template("signup.html", text="请填入密码")
    
            user = User.query.filter(User.id == userid).first()
            if (user):
                return render_template("signup.html", text="该用户已经注册")
            elif (password != password2):
                return render_template("signup.html", text="两次密码不同，请核对")
            else:
                user = User(id=userid, usertype=identity, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
    
        return redirect(url_for("auth.login"))
    
    
    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template("login.html")
        else:
            userid = request.form.get('userid')
            password_input = request.form.get('password')
            user = User.query.filter(User.id == userid).first()
    
            if user == None:
                return render_template("login.html", text="请先注册")
            if not check_password_hash(user.password, password_input):
                return render_template("login.html", text="密码错误")
            
        session['user_id'] = user.id
        session['usertype'] = user.usertype
        return redirect(url_for("space.personal_page",id=userid))
    
    
    @bp.before_app_request
    def load_logged_in_user():
        try:
            user_id = session['user_id']
            user_type = session['usertype']
        except:
            user_id = None
            user_type = None
    
        if user_id is None:
            g.user = None
            g.usertype = None
        else:
            g.user = User.query.filter(User.id == user_id)
            g.usertype = user_type
            g.userid = user_id
    
    
    @bp.route('/logout',methods=['GET','POST'])
    def logout():
        try:
            session.pop('user_id')
            session.pop('usertype')
        except:
            pass
        g.user = None
        g.usertype = None
        g.userid = None
        return redirect(url_for('home'))
    
    
    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                flash('You need to login first.')
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view
    
  ```
  
  
  
- [config.py](https://github.com/yuanyangwangTJ/website/blob/master/app/config.py)
  
  ```python
    #flask
    DEBUG = True
    #session
    SECRET_KEY="1145141919810"
    
    #mysql
    DIQLECT = "mysql"
    DRIVER="pymysql"
    USERNAME = "root"
    PASSWORD = "root"
    HOST = "127.0.0.1"
    PORT = "3306"
    DATABASE = "CSBIGHW"
    
    
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIQLECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    
  ```
  
  
  
- [databases.py](https://github.com/yuanyangwangTJ/website/blob/master/app/databases.py)
  
  ```python
    from flask_sqlalchemy import SQLAlchemy
    
    db = SQLAlchemy()
    
    TEMPLATE_FOLDER = '../templates'
    STATIC_FOLDER = '../static'
    UPLOAD_FOLDER = '../upload'
    
    # TO-DO add the database detail column
    class User(db.Model):
        __tablename__ = 'User'
        id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
        usertype = db.Column(db.Enum('student', 'teacher', 'admin'),
                         nullable=False, default='student')
        password = db.Column(db.Text, nullable=False)
        profile_image_path = db.Column(db.String(255))
        profile_image_name = db.Column(db.String(255))
    
    #存放报名信息
    tags = db.Table('tags',
        db.Column('User_id', db.Integer, db.ForeignKey('User.id')),
        db.Column('Activity_id', db.Integer, db.ForeignKey('Activity.id'))
    )
    
    class Activity(db.Model):
        __tablename__ = 'Activity'
        id = db.Column(db.Integer, primary_key=True,
                       nullable=False, autoincrement=True)
        name = db.Column(db.String(255), nullable=False)
        description = db.Column(db.String(255))
        cover_image_path = db.Column(db.String(255))
        cover_image_name = db.Column(db.String(255))
        label = db.Column(db.Enum('virtue', 'wisdom', 'body',
                                  'beauty', 'labor'), nullable=False)
    
        # start_time = db.Column(db.DateTime, nullable=False)
        # end_time = db.Column(db.DateTime, nullable=False)
        lead_teacher = db.Column(db.String(255), nullable=False)
        # cover_path = db.Column(db.Text)
        # max_join = db.Column(db.Integer, default=999)
        # current_join = db.Column(db.Integer, default=0)
        score = db.Column(db.Integer, default=1)
        participants = db.relationship('User', secondary=tags,
            backref=db.backref('activities', lazy='dynamic'))
        status = db.Column(db.Enum('coming', 'finished'), default='coming')
    
    
    
  ```
  
  
  
- [image.py](https://github.com/yuanyangwangTJ/website/blob/master/app/image.py)
  
  ```python
    import time
    import os
    import datetime
    import random
    
    from werkzeug.utils import secure_filename
    from flask import Flask, Blueprint, render_template, redirect,request, url_for, make_response, send_from_directory, abort, session, flash, g
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
                return redirect(url_for('space.personal_page'))
            else:
                flash('The image format is not supported. Please try again.')
                render_template('./pages/user.html')
    
    
    
    # display different users profile image in comments etc.
    # return the relative path of the image
    def profile_image_directory(user_id):
        user = User.query.fliter(User.id == user_id)
        if user is None:
            return None
        else:
            # TO-DO edit the iamge path for frontend to find the image
            return os.path.join('../../website',user.profile_image_directory, user.profile_image_name)
    
    
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
    
    
  ```
  
  
  
- [module.py](https://github.com/yuanyangwangTJ/website/blob/master/app/module.py)
  
  ```python
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
    
    
  ```
  
  
  
- [space.py](https://github.com/yuanyangwangTJ/website/blob/master/app/space.py)
  
  ```python
    import os
    import datetime
    from flask import Flask, Blueprint, url_for, render_template, request, make_response, redirect, abort, session, flash, g
    from flask_sqlalchemy import SQLAlchemy
    import base64
    
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
    
    def generate_profile_image_path(user):
        return os.path.join(user.profile_image_path, user.profile_image_name)
    
    def image_stream(path):
        image_stream = ''
        with open(path, 'rb') as image_f:
            image_stream = image_f.read()
            image_stream = base64.b64encode(image_stream)
        return image_stream
    
    
    bp = Blueprint('space', __name__)
    
    @bp.route('/user/', methods=['GET', 'POST'])
    @login_required
    def personal_page():
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return render_template('pages/user.html', user_id=None,
                                    profile_image_path=None, user=None,
                                    scores={'virtue': 0, 'wisdom': 0, 'body': 0, 'beauty': 0, 'labor': 0})
    
        if not (user.profile_image_path and user.profile_image_name):
            profile_image = ''
        else:
            profile_image = image_stream(generate_profile_image_path(user))
            
        if(user.usertype == 'student'):
            scores = stat_scores(user)
            total_score = scores['virtue'] + scores['wisdom'] + scores['body'] + scores['beauty'] + scores['labor']
            return render_template('pages/user.html', user_id=user_id,
                                    profile_image=profile_image, user=user,
                                    scores=scores, total_score=total_score)
        else:
            return render_template('teacher/base.html', user_id=user_id,
                                   profile_image=profile_image, user=user)
    
    
    @bp.route('/user/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        
        if not (user.profile_image_path and user.profile_image_name):
            profile_image = None
        else:
            profile_image = image_stream(generate_profile_image_path(user))
        
        if request.method == 'GET':
            if user.usertype == 'student':
                return render_template('pages/profile.html', user_id=user_id,
                                       profile_image=profile_image, user=user)
            else:
                return render_template('teacher/profile.html', user_id=user_id,
                                       profile_image=profile_image, user=user)
    
    
    
    
  ```
  
  
  
- **前端**

  - **pages**：此处为前端学生的网页设计

    - [profile.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/pages/profile.html)
  
    ```jinja2
      {% extends 'pages/user.html' %}
    
      <!-- 这是一个用 jinja2 从Base.html渲染得到的实例 需要启动 flask 环境后才能看到-->
      <!-- 这样可以避免一项修改多处寻找 -->
      
      {% block title %}
    Profile
      {% endblock title %}
    
      {% block content %}
    
      <div class="page-header">
        <div class="row">
              <div class="col-md-6 col-sm-12">
                <div class="title">
                      <h4>Upload Profile Image</h4>
                </div>
                  <nav aria-label="breadcrumb" role="navigation">
                    <ol class="breadcrumb">
                          <li class="breadcrumb-item"><a href="../index.html">Home</a></li>
                        <li class="breadcrumb-item active" aria-current="page">Profile</li>
                      </ol>
                </nav>
              </div>
    
              <!--此处为选项-->
            <div class="col-md-6 col-sm-12 text-right">
                  <div class="dropdown">
                    <form action="{{ url_for('image.profile_image_upload') }}" method="POST" enctype="multipart/form-data">
                          <input type="file" name="image" id="image" accept="image/*">
                          <button class="btn btn-primary">upload</button>
                          <p class="message"></p>
                      </form>
                  </div>
              </div>
          </div>
      </div>
      
      {% endblock content %}
    ```
  
      
  
    - [user.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/pages/user.html)
  
      ```jinjia2
      <!-----------------------
      Name: user.html
      Function: 个人用户界面
      Author: king
      ------------------------>
      
      <!DOCTYPE html>
      <html>
      
      <head>
      	<!-- Basic Page Info -->
      	<meta charset="utf-8">
      	{% block header %}
      	<title>Personal Data</title>
      	{% endblock header %}
      
      	<!-- Mobile Specific Metas -->
      	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
      	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      	<meta http-equiv="imagetoolbar" content="no" />
      
      	<!-- CSS -->
      	<link rel="stylesheet" type="text/css" href="../../static/css/style.css">
      	<link rel="stylesheet" type="text/css" href="../../static/styles/core.css">     
      	<link rel="stylesheet" type="text/css" href="../../static/styles/icon-font.min.css">
      	<link rel="stylesheet" type="text/css" href="../../static/styles/style.css">     
      	<link rel="stylesheet" href="../../static/css/layout.css" type="text/css" />
      	<link rel="stylesheet" href="../../static/css/bootstrap/bootstrap.min.css">
      
      	<!--Get time-->
      	<script>
      		window.dataLayer = window.dataLayer || [];
      		function gtag() { dataLayer.push(arguments); }
      		gtag('js', new Date());
      		gtag('config', 'UA-119386393-1');
      	</script>
      </head>
      <!-- ####################################################################################################### -->
      
      <body id="top">
      	<div class="wrapper row1">
      		<div id="header" class="clear">
      			<div class="fl_left">
      				<h1><a href={{url_for('home')}}>Second Classroom</a></h1>
      				<p>College of Electronics and Information Engineering</p>
      			</div>
      			<!--以下几个部分关于右上角，除Home外其他待修改-->
      			<div class="fl_right">
      				<ul>
      					<li><a href={{url_for('home')}}>Home</a></li>
      					{% if g.userid %}
      					<li class="last">{{g.userid}}</li>
      					<li class="last"><a href={{url_for('auth.logout')}}>Logout Here</a></li>
      					{% else %}
      					<li class="last"><a href={{url_for('auth.login')}}>Login Here</a></li>
      					{%endif%}
      				</ul>
      				<form action="#" method="post" id="sitesearch">
      					<fieldset>
      						<strong>Search:</strong>
      						<input type="text" value="Search Our Website&hellip;"
      							onfocus="this.value=(this.value=='Search Our Website&hellip;')? '' : this.value ;" />
      						<input type="image" src="../static/img/search.gif" id="search" alt="Search" />
      					</fieldset>
      				</form>
      			</div>
      		</div>
      	</div>
      	<!--以上部分为网页上端部分，各个网页关于上端部分应该相同，故修改上面部分仍何地方后要在wisdom,body等html文件中同步修改-->
      	<!--五育页面格式相同，彼此也要同步修改-->
      	<!-- ####################################################################################################### -->
      	<!--以下为导航栏,导航栏遇到的问题是文字过于居中，应该令其两侧对齐，css文件在navi.css里topnav处-->
      	<div class="wrapper row2">
      		<div class="rnd">
      			<!-- ###### -->
      			<div id="topnav">
      				<ul>
      					<li><a href={{url_for('home')}}>Home</a></li>
      					<li><a href={{url_for('module.virtue')}}>Morality Activity</a></li>
      					<li><a href={{url_for('module.wisdom')}}>Wisdom Activity</a></li>
      					<li><a href={{url_for('module.body_act')}}>Sports Activity</a></li>
      					<li><a href={{url_for('module.beauty')}}>Arts Activity</a></li>
      					<li><a href={{url_for('module.labor')}}>Labor Activity</a></li>
      					<li class="active"><a href={{url_for('space.personal_page')}}>User Page</a></li>
      					<!--个人建议将首页放在这里，但也有人提议放在其他地方-->
      				</ul>
      			</div>
      			<!-- ###### -->
      		</div>
      	</div>
      	<!-- ####################################################################################################### -->
      	<!--日历小挂件-->
      	<div class="canlenda">
      		<div class="col-md-4 col-sm-12 text-center">
      			<div class="mb-20">
      				<div class="datepicker-here" data-timepicker="true" data-language='en'></div>
      			</div>
      		</div>
      	</div>
      
      	<!--主体内容，显示德育分数-->
      	<!--begin main-container-->
      	<div class="mobile-menu-overlay"></div>
      	<div class="main-container">
      		<div class="xs-pd-20-10 pd-ltr-20">
      			<div class="page-header">
      				<div class="row">
      					<div class="col-md-6 col-sm-12">
      						<div class="title">
      							<h4>Your Score</h4>
      						</div>
      						<nav aria-label="breadcrumb" role="navigation">
      							<ol class="breadcrumb">
      								<li class="breadcrumb-item"><a href="../index.html">Home</a></li>
      								<li class="breadcrumb-item active" aria-current="page">Your Score</li>
      							</ol>
      						</nav>
      					</div>
      
      					<!--此处为选项-->
      					<div class="col-md-6 col-sm-12 text-right">
      						<div class="dropdown">
      							<a class="btn btn-primary" href={{url_for('space.personal_page')}} role="button">
      								Score
      							</a>
      							<a class="btn btn-primary" href={{url_for('space.profile')}} role="button">
      								Profile
      							</a>
      						</div>
      					</div>
      				</div>
      			</div>
      
      			{% block content %}
      
      			<div class="row clearfix progress-box">
      				<!--本行的作用为保证各个模块横排-->
      
      				<!--显示各个模块的分数，注意接口的分数以及百分比的计算-->
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-blue padding-top-10 h5">Virtue Score</h5>
      							<span class="d-block">{{scores['virtue']}} <br><i class="fa fa-line-chart text-blue"></i></span>
      						</div>
      					</div>
      				</div>
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-green padding-top-10 h5">Wisdom Score</h5>
      							<span class="d-block">{{scores['wisdom']}} <br><i class="fa text-light-green fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-orange padding-top-10 h5">Body Score</h5>
      							<span class="d-block">{{scores['body']}} <br><i class="fa text-light-orange fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-purple padding-top-10 h5">Beauty Score</h5>
      							<span class="d-block">{{scores['beauty']}} <br><i class="fa text-light-purple fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-blue padding-top-10 h5">Labor Score</h5>
      							<span class="d-block">{{scores['labor']}} <br><i class="fa fa-line-chart text-blue"></i></span>
      						</div>
      					</div>
      				</div>
      
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-purple padding-top-10 h5">Total Score</h5>
      							<span class="d-block">{{total_score}} <br><i class="fa text-light-purple fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-orange padding-top-10 h5">Rest Score</h5>
      							<span class="d-block">{{100 - total_score if total_score <= 100 else 0}} <br><i class="fa text-light-orange fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      			</div>
      			{% endblock content %}
      
      			<!-- ####################################################################################################### -->
      			<!--此处用来打表，将该名用户报名活动输出出来-->
      
      			<!-- ####################################################################################################### -->
      			<div class="wrapper row4">
      				<div class="rnd">
      					<div id="footer" class="clear">
      						<!-- ####################################################################################################### -->
      						<div class="fl_left clear">
      							<!--高德地图链接-->
      							<div class="fl_left center"><img src="../static/img/demo/worldmap.gif" alt="" /><br />
      								<a
      									href="https://www.amap.com/search?id=B00155HU50&city=310114&geoobj=121.447275%7C31.268923%7C121.458199%7C31.274481&query_type=IDQ&query=%E5%90%8C%E6%B5%8E%E5%A4%A7%E5%AD%A6%E5%98%89%E5%AE%9A%E6%A0%A1%E5%8C%BA&zoom=17.5">
      									Find Us With AMap &raquo;</a>
      							</div>
      							<address>
      								Address Line 1: Tongji University<br />
      								Address Line 2: 4800, Cao'an Road, Huangdu Town, Jiading District<br />
      								City: Shanghai City<br />
      								Postcode: 200000<br />
      								<br />
      								Tel: (021)69589979<br />
      								Email: <a href="mailto:dxwg@tongji.edu.cn">dxwg@tongji.edu.cn</a>
      							</address>
      						</div>
      						<!-- ####################################################################################################### -->
      					</div>
      				</div>
      			</div>
      			<!-- ####################################################################################################### -->
      		</div>
      	</div>
      	<!-- js -->
      	<!--日历启动的核心js-->
      	<script src="../../static/js/core.js"></script>
      
      </body>
      </html>
      ```
  
      
  
  - **teacher**：教师端的网页设计
  
    - [base.html](https://github.com/yuanyangwangTJ/website/tree/master/templates/teacher/base.html)
  
      ```jinjia2
      <!-----------------------
      Name: user.html
      Function: 教师用户界面
      Author: king
      ------------------------>
      
      <!DOCTYPE html>
      <html>
      
      <head>
      	<!-- Basic Page Info -->
      	<meta charset="utf-8">
      	<title>Administrator</title>
      
      	<!-- Mobile Specific Metas -->
      	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
      
      	<!-- CSS -->
      	<link rel="stylesheet" type="text/css" href="../../static/css/style.css">
      	
      	<link rel="stylesheet" type="text/css" href="../../static/styles/core.css">
      	<link rel="stylesheet" type="text/css" href="../../static/styles/icon-font.min.css">
      	<link rel="stylesheet" type="text/css" href="../../static/styles/style.css">
      	<link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
      	
      
      	<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
      	<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
      	<!--Get time-->
      	<script>
      		window.dataLayer = window.dataLayer || [];
      		function gtag() { dataLayer.push(arguments); }
      		gtag('js', new Date());
      		gtag('config', 'UA-119386393-1');
      	</script>
      </head>
      
      <body>
      	<!--导航栏的头部，非特殊情况不考虑模板替换-->
      	<div class="header">
      		<!--begin header-left-->
      		<div class="header-left">
      			<div class="menu-icon dw dw-menu"></div>
      			<!--搜索框以及搜索按钮(按钮在向下箭头下面)-->
      			<div class="search-toggle-icon dw dw-search2" data-toggle="header_search"></div>
      			<div class="header-search">
      				<form>
      					<div class="form-group mb-0">
      						<i class="dw dw-search2 search-icon"></i>
      						<input type="text" class="form-control search-input" placeholder="Search Here">
      						<div class="dropdown">
      							<a class="dropdown-toggle no-arrow" href="#" role="button" data-toggle="dropdown">
      								<i class="ion-arrow-down-c"></i>
      							</a>
      							<div class="dropdown-menu dropdown-menu-right">
      								<div class="text-right">
      									<button class="btn btn-primary">Search</button>
      								</div>
      							</div>
      						</div>
      					</div>
      				</form>
      			</div>
      		</div>
      		<!--end header-left-->
      
      		<!--begin header-right-->
      		<div class="header-right">
      			<!--用户通知部分-->
      			<div class="dashboard-setting user-notification">
      				<div class="dropdown">
      					<a class="dropdown-toggle no-arrow" href="javascript:;" data-toggle="right-sidebar">
      						<i class="dw dw-settings2"></i>
      					</a>
      				</div>
      			</div>
      			<div class="user-notification">
      				<div class="dropdown">
      					<a class="dropdown-toggle no-arrow" href="#" role="button" data-toggle="dropdown">
      						<i class="icon-copy dw dw-notification"></i>
      						<span class="badge notification-active"></span>
      					</a>
      					<div class="dropdown-menu dropdown-menu-right">
      						<div class="notification-list mx-h-350 customscroll">
      							<ul>
      								<li>
      									<a href="#">
      										<p>Please note the notice</p>
      									</a>
      								</li>
      							</ul>
      						</div>
      					</div>
      				</div>
      			</div>
      
      			<div class="user-info-dropdown">
      				<div class="dropdown">
      					<a class="dropdown-toggle" href="#" role="button" data-toggle="dropdown">
      						<span class="user-icon">
      							{% if profile_image_path == None %}
      								<img src="../../static/img/photo1.jpg" alt="">
      							{% else %}
      								<img src="data:;base64,{{ profile_image }}" alt="">
      							{% endif %}
      
      							<!--此处为用户的头像，我们显示默认头像-->
      							
      						</span>
      						<!--此处显示用户名-->
      						<span class="user-name">{{user_id}}</span>
      					</a>
      					<!--此处的退出登录按钮后端需要考虑一下设置-->
      					<div class="dropdown-menu dropdown-menu-right dropdown-menu-icon-list">
      						<a class="dropdown-item" href={{url_for('space.profile')}}><i class="dw dw-logout"></i> Profile</a>
      						<a class="dropdown-item" href={{url_for('auth.logout')}}><i class="dw dw-logout"></i> Log Out</a>
      					</div>
      				</div>
      			</div>
      		</div>
      		<!--end header-right-->
      	</div>
      
      	<!--为个人界面的主题设置，后端不需要考虑更改-->
      	<!--begin right-sidebar-->
      	<div class="right-sidebar">
      		<div class="sidebar-title">
      			<h3 class="weight-600 font-16 text-blue">
      				Layout Settings
      				<span class="btn-block font-weight-400 font-12">User Interface Settings</span>
      			</h3>
      			<div class="close-sidebar" data-toggle="right-sidebar-close">
      				<i class="icon-copy ion-close-round"></i>
      			</div>
      		</div>
      		<div class="right-sidebar-body customscroll">
      			<div class="right-sidebar-body-content">
      				<h4 class="weight-600 font-18 pb-10">Header Background</h4>
      				<div class="sidebar-btn-group pb-30 mb-10">
      					<a href="javascript:void(0);" class="btn btn-outline-primary header-white active">White</a>
      					<a href="javascript:void(0);" class="btn btn-outline-primary header-dark">Dark</a>
      				</div>
      
      				<h4 class="weight-600 font-18 pb-10">Sidebar Background</h4>
      				<div class="sidebar-btn-group pb-30 mb-10">
      					<a href="javascript:void(0);" class="btn btn-outline-primary sidebar-light ">White</a>
      					<a href="javascript:void(0);" class="btn btn-outline-primary sidebar-dark active">Dark</a>
      				</div>
      
      				<div class="reset-options pt-30 text-center">
      					<button class="btn btn-danger" id="reset-settings">Reset Settings</button>
      				</div>
      			</div>
      		</div>
      	</div>
      	<!--end right-sidebar-->
      
      	<!--begin left-side-bar-->
      	<div class="left-side-bar">
      		<!--此处为logo显示界面-->
      		<div class="brand-logo">
      			<a href="user.html">
      				<img src="../../static/img/tongji-logo.svg" alt="" class="dark-logo">
      				<img src="../../static/img/tongji-logo-white.jpg" alt="" class="light-logo">
      			</a>
      			<div class="close-sidebar" data-toggle="left-sidebar-close">
      				<i class="ion-close-round"></i>
      			</div>
      		</div>
      		<div class="menu-block customscroll">
      			<div class="sidebar-menu">
      				<ul id="accordion-menu">
      					<!--home 界面可以显示学生申请活动的情况，教师可以进行活动审批-->
      					<li>
      						<a href={{ url_for("space.personal_page")}} class="dropdown-toggle no-arrow">
      							<span class="micon dw dw-calendar1"></span><span class="mtext">Home</span>
      						</a>
      					</li>
      
      					<!--教师发布活动处-->
      					<li>
      						<a href={{url_for('act.new')}}  class="dropdown-toggle no-arrow">
      
      							<span class="micon dw dw-calendar1"></span><span class="mtext">Create Activity</span>
      						</a>
      					</li>
      
      					<!--下面为教师审批功能，对学生提交的活动进行审批-->
      					<!--教师可以观看各个板块活动的提交情况-->
      					<li class="dropdown">
      						<a href={{url_for('module.virtue')}} class="dropdown-toggle">
      							<span class="micon dw dw-paint-brush"></span><span class="mtext">Morality Moudle</span>
      						</a>
      					</li>
      					<li class="dropdown">
      						<a href={{url_for('module.wisdom')}} class="dropdown-toggle">
      							<span class="micon dw dw-paint-brush"></span><span class="mtext">Wisdom Moudle</span>
      						</a>
      					</li>
      					<li class="dropdown">
      						<a href={{url_for('module.body_act')}} class="dropdown-toggle">
      							<span class="micon dw dw-paint-brush"></span><span class="mtext">Sports Moudle</span>
      						</a>
      					</li>
      					<li class="dropdown">
      						<a href={{url_for('module.beauty')}} class="dropdown-toggle">
      							<span class="micon dw dw-paint-brush"></span><span class="mtext">Arts Moudle</span>
      						</a>
      					</li>
      					<li class="dropdown">
      						<a href={{url_for('module.labor')}} class="dropdown-toggle">
      							<span class="micon dw dw-paint-brush"></span><span class="mtext">Labor Moudle</span>
      						</a>
      					</li>
      
      					<li>
      						<div class="sidebar-small-cap">Extra</div>
      					</li>
      					<!--联系我们，加上联系方式-->
      					<li>
      						<a href="javascript:;" class="dropdown-toggle">
      							<span class="micon dw dw-edit-2"></span><span class="mtext">Contact us</span>
      						</a>
      					</li>
      					<!--返回Home界面-->
      					<li>
      						<a href={{url_for('home')}} class="dropdown-toggle no-arrow">
      							<span class="micon dw dw-calendar1"></span><span class="mtext">Return</span>
      						</a>
      					</li>
      				</ul>
      			</div>
      		</div>
      	</div>
      
      	<!--主题内容，可以显示标题栏的具体活动内容-->
      	<!--begin main-container-->
      	<!--此处为页面核心部分，需要修改替换-->
      	<div class="mobile-menu-overlay"></div>
      	<div class="teacher_main-container">
      		<div class="xs-pd-20-10 pd-ltr-20">
      			<div class="page-header">
      				<div class="row">
      					<div class="col-md-6 col-sm-12">
      						<div class="title">
      							<h4>{% block page_item %} Moral Education {% endblock page_item %}</h4>
      						</div>
      						<nav aria-label="breadcrumb" role="navigation">
      							<ol class="breadcrumb">
      								<li class="breadcrumb-item"><a href={{url_for('home')}}>Home</a></li>
      								<li class="breadcrumb-item active" aria-current="page">{% block active_item %}Activity{% endblock active_item %}</li>
      							</ol>
      						</nav>
      					</div>
      					{% block menu_item %}
      					<!--在此处显示时间-->
      					<div class="col-md-6 col-sm-12 text-right">
      						<div class="dropdown">
      							<a class="btn btn-primary dropdown-toggle" href="#" role="button" data-toggle="dropdown">
      								December 2020
      							</a>
      						</div>
      					</div>
      					{% endblock menu_item %}
      				</div>
      			</div>
      
      			<div class="row clearfix progress-box">
      
      				{% block main_content %}
      
      				<!--注意此处main-content 与 main-container的区别-->
      				<!-----------------------------------------
      				这之间为活动的主体内容设置
      				------------------------------------------->
      				<!-- 进度表，装饰作用-->
      				
      				
      				<div class="panel panel-info" style="margin: 0 100px;">
      					<div class="panel-heading">
      						<h3 class="panel-title">Function Introduction</h3>
      					</div>
      					<div class="panel-body">
      						<p>You can finish some operations on this page.</p>
      					</div>
      					<ul class="list-group">
      						<li class="list-group-item">Public Activity</li>
      						<li class="list-group-item">Morality Activity</li>
      						<li class="list-group-item">Wisdom Activity</li>
      						<li class="list-group-item">Sports Activity</li>
      						<li class="list-group-item">Arts Activity</li>
      						<li class="list-group-item">Labor Activity</li>
      					</ul>
      				</div>
      
      				{% endblock main_content %}
      
      			</div>
      		</div>
      	</div>
      		<!-- js -->
      		<script src="../../static/js/core.js"></script>
      		<script src="../../static/js/layout-settings.js"></script>
      </body>
      </html>
      ```
  
      
  
    - [profile.html](https://github.com/yuanyangwangTJ/website/tree/master/templates/teacher/profile.html)：个人头像修改网页
  
      ```jinja2
      {% extends 'teacher/base.html' %}
      
      {% block page_item %}
          My Profile
      {% endblock page_item %}
      
      {% block active_item %}
          Profile
      {% endblock active_item %}
      
      {% block menu_item %}
          <!--此处为选项-->
          <div class="col-md-6 col-sm-12 text-right">
              <div class="dropdown">
                  <form action="{{ url_for('image.profile_image_upload') }}" method="POST" enctype="multipart/form-data">
                      <input type="file" name="image" id="image" accept="image/*">
                      <button class="btn btn-primary">upload</button>
                      <p class="message"></p>
                  </form>
              </div>
          </div>
      {% endblock menu_item %}
      ```
  
      
  
    - [pubActivity.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/teacher/pubActivity.html)：发布活动网页
  
      ```jinja2
      <!---------------------------------
      Name: pubActivity.html
      Function: 教师(管理员)发布活动
      Author: king
      Ps: Jinja2模板网站，以base.html为基础
      ----------------------------------->
      
      {% extends 'teacher/base.html' %}
      
      {% block page_item %}
          Moral Education
      {% endblock page_item %}
      
      {% block active_item %}
          Public Activity
      {% endblock active_item %}
      
      {% block main_content %}
      <!-- 下面为教师管理员发布活动的具体提交框，包括模块，标题，带队教师，分数，介绍，活动封面-->
      <div class="file-submit">
          <div class="panel panel-success">
              <div class="panel-heading">
                  <h3 class="panel-title">Public Activity</h3>
              </div><br>
      
              <!-- 设置提交的内容 -->
              <div class="public-activity">
                  <!-- form设置前后端连接的方式 -->
              <form action="{{ url_for('act.new')}}" method="POST" enctype="multipart/form-data">
                  <!-- 活动选择-->
                  <!-- 从五大模块中选择一个，五选一，默认为virtue -->
                   <label for="activity-select" >Choose a activity module:</label>
                      <select class="activity-select" name="label">
                          <option value="virtue" selected>virtue</option>
                          <option value="wisdom">wisdom</option>
                          <option value="body">body</option>
                          <option value="beauty">beauty</option>
                          <option value="labor">labor</option>
                      </select> 
                  <br><br>
      
                  <!-- 活动的标题上传 -->
                  <!-- 设置的{{text}}为错误信息反馈 -->
                  <label for="activity-select">Activity Tittle</label>
                  <div class="form-group">
                      <input type="text" class="form-control" id="name" name="name" style="width: 400px;"
                      placeholder="Please input activity tittle">{{text}}
                  </div>
      
                  <!-- 活动的领队教师设置 -->
                  <label for="activity-select">Activity Teacher</label>
                  <div class="form-group">
                      <input type="text" class="form-control" id="name" style="width: 250px;"
                      placeholder="Please input activity teacher" name="lead_teacher">{{text}}
                  </div>
      
                  <!-- 活动的分数设置 -->
                  <!-- 此处已经由前端代码判断输入是否为数字，后端只需要考虑分数的高低限制（或者不设）-->
                  <label for="activity-select">Activity Score</label>
                  <div class="form-group">
                      <input type="text" name="score" onkeyup="this.value=this.value.replace(/\D/g,'')"
                      class="form-control" id="name" style="width: 250px;"
                      placeholder="Please input activity score">{{text}}
                  </div>
      
                  <!-- 活动的介绍 -->
                  <!-- 描述活动的具体内容 -->
                  <label for="activity-select">Activity Describe</label>
                  <div class="form-group">
                      <textarea class="form-control" rows="3" name="description">{{text}}</textarea>
                  </div>
      
                  <!-- 活动封面图 -->
                  <!-- 此处上传活动的封面图，可以在前端显示-->
                  <div class="panel-body">
                      <!--此处接受图像文件，限定为图片格式-->
                      <input type="file" name="image" id="image" accept="image/*"><br>
                  </div>
      
                  <!-- upload上传按钮 -->
                  <input type="submit" value="upload">
                   <!-- <button type="button" class="btn btn-secondary">upload</button> -->
                  <p class="message"></p>
      
              </form>
              </div>
          </div>
      </div>
      
      <!-- 日历挂件-->
      <div class="canlenda2">
          <div class="col-md-4 col-sm-12 text-center">
              <div class="mb-20">
                  <div class="datepicker-here" data-timepicker="true" data-language='en'></div>
              </div>
          </div>
      </div>
      
      {% endblock main_content %}
      ```
  
      
  
    - [reviseActivity.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/teacher/reviseActivity.html)：修改活动网页
  
      ```jinja2
      <!---------------------------------
      Name: pubActivity.html
    Function: 教师(管理员)发布活动
      Author: king
      Ps: Jinja2模板网站，以base.html为基础
      ----------------------------------->
      
      {% extends 'teacher/base.html' %}
      
      {% block page_item %}
          Moral Education
      {% endblock page_item %}
      
      {% block active_item %}
          Revise Activity
      {% endblock active_item %}
      
      {% block main_content %}
      <!-- 下面为教师管理员发布活动的具体提交框，包括模块，标题，带队教师，分数，介绍，活动封面-->
      <div class="file-submit">
          <div class="panel panel-success">
              <div class="panel-heading">
                  <h3 class="panel-title">Revise Activity</h3>
              </div><br>
      
              <!-- 设置提交的内容 -->
              <div class="public-activity">
                  <!-- form设置前后端连接的方式 -->
              <form action="{{ url_for('act.revise', activity_id=activity_id)}}" method="POST" enctype="multipart/form-data">
                  <!-- 活动选择-->
                  <!-- 从五大模块中选择一个，五选一，默认为virtue -->
                   <label for="activity-select" >Choose a activity module:</label>
                      <select class="activity-select" name="label">
                          <option value="virtue" selected>virtue</option>
                          <option value="wisdom">wisdom</option>
                          <option value="body">body</option>
                          <option value="beauty">beauty</option>
                          <option value="labor">labor</option>
                      </select> 
                  <br><br>
      
                  <!-- 活动的标题上传 -->
                  <!-- 设置的{{text}}为错误信息反馈 -->
                  <label for="activity-select">Activity Tittle</label>
                  <div class="form-group">
                      <input type="text" class="form-control" name="name" style="width: 400px;"
                      value={{act.name}}>
                  </div>
      
                  <!-- 活动的领队教师设置 -->
                  <label for="activity-select">Activity Teacher</label>
                  <div class="form-group">
                      <input type="text" class="form-control" style="width: 250px;"
                      value={{act.lead_teacher}} name="lead_teacher">
                  </div>
      
                  <!-- 活动的分数设置 -->
                  <!-- 此处已经由前端代码判断输入是否为数字，后端只需要考虑分数的高低限制（或者不设）-->
                  <label for="activity-select">Activity Score</label>
                  <div class="form-group">
                      <input type="text" name="score" onkeyup="this.value=this.value.replace(/\D/g,'')"
                      class="form-control" id="name" style="width: 250px;"
                      value={{act.score}}>
                  </div>
      
                  <!-- 活动的介绍 -->
                  <!-- 描述活动的具体内容 -->
                  <label for="activity-select">Activity Describe</label>
                  <div class="form-group">
                      <textarea class="form-control" rows="3" name="description">{{act.description}}</textarea>
                  </div>
      
                  <!-- 活动封面图 -->
                  <!-- 此处上传活动的封面图，可以在前端显示-->
                  <div class="panel-body">
                      <!--此处接受图像文件，限定为图片格式-->
                      <input type="file" name="image" id="image" accept="image/*"><br>
                  </div>
      
                  <!-- upload上传按钮 -->
                  <input type="submit" value="upload">
                   <!-- <button type="button" class="btn btn-secondary">upload</button> -->
                  <p class="message"></p>
      
              </form>
              </div>
          </div>
      </div>
      
      <!-- 日历挂件-->
      <div class="canlenda2">
          <div class="col-md-4 col-sm-12 text-center">
              <div class="mb-20">
                  <div class="datepicker-here" data-timepicker="true" data-language='en'></div>
              </div>
          </div>
      </div>
      
      {% endblock main_content %}
      ```
      
      
  
  - [Base.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/Base.html) ：首页模板网页
  
      ```jinja2
      <!DOCTYPE html>
      <!-- 这是jinja2模板的基础页面 -->
      <html>
      <head>
      {% block head %}
          <title>Second Classroom | {% block title %}Base{% endblock title %} </title>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
          <meta http-equiv="imagetoolbar" content="no" />
          <link rel="stylesheet" href="../static/css/layout.css" type="text/css" />
      {% endblock head %}
      </head>
      
      <body id="top">
          <div class="wrapper row1">
              <div id="header" class="clear">
                  <div class="fl_left">
                      <h1><a href={{url_for('home')}}>Second Classroom</a></h1>
                      <p>College of Electronics and Information Engineering</p>
                  </div>
      
                  <div class="fl_right">
                      <ul>
                          <li><a href={{url_for('home')}}>Home</a></li>
                          {% if g.userid %}
      					<li class="last">{{g.userid}}</li>
      					<li class="last"><a href={{url_for('auth.logout')}}>Logout Here</a></li>
      		  
      					{% else %}
      					<li class="last"><a href={{url_for('auth.login')}}>Login Here</a></li>
      					{%endif%}
                      </ul>
                      <!-- TO-DO 完成后端搜索框前端适配 -->
                      <form action="#" method="post" id="sitesearch">
                          <fieldset>
                              <strong>Search:</strong>
                              <input type="text" value="Search Our Website&hellip;"
                                  onfocus="this.value=(this.value=='Search Our Website&hellip;')? '' : this.value ;" />
                              <input type="image" src="../static/img/search.gif" id="search" alt="Search" />
                          </fieldset>
                      </form>
                  </div>
              </div>
          </div>
          <!-- ####################################################################################################### -->
          <div class="wrapper row2">
              <div class="rnd">
                  <!-- ###### -->
                  <div id="topnav">
                      <ul>
                          {% block topnavi %}
                              <li><a href={{url_for('home')}}>Home</a></li>
                              <li><a href={{url_for('module.virtue')}}>Morality Activity</a></li>
                              <li><a href={{url_for('module.wisdom')}}>Wisdom Activity</a></li>
                              <li><a href={{url_for('module.body_act')}}>Sports Activity</a></li>
                              <li><a href={{url_for('module.beauty')}}>Arts Activity</a></li>
                              <li><a href={{url_for('module.labor')}}>Labor Activity</a></li>
                              <li class="last"><a href={{url_for('space.personal_page')}}>User Page</a></li>
                          {% endblock topnavi %}
                      </ul>
                  </div>
                  <!-- ###### -->
              </div>
          </div>
          <!-- ####################################################################################################### -->
          <!--日历小挂件-->
      	<div class="canlenda">
      		<div class="col-md-4 col-sm-12 text-center">
      			<div class="mb-20">
      				<div class="datepicker-here" data-timepicker="true" data-language='en'></div>
      			</div>
      		</div>
          </div>
          
          <div class="wrapper row3">
              <div class="rnd">
                  <div id="container" class="clear">
                      <!-- ####################################################################################################### -->
                      <!--此处为活动页面，应该从后端数据库读取数据，然后全部加载出来-->
      
                      {% block content %}
                      <div id="portfolio">
                          <ul>
                              <li><img src="../static/img/demo/420x190.gif" alt="" />
                                  <h2>Metridiculis conseque quis</h2>
                                  <p>Orciinterdum condimenterdum nullamcorper elit nam curabitur laoreet met praesenean et
                                      iaculum. Metridiculis conseque quis iaculum aenean nunc aenean quis nam nis dui.</p>
                                  <p class="readmore"><a href="#">Read More Here &raquo;</a></p>
                              </li>
                              <li class="last"><img src="../static/img/demo/420x190.gif" alt="" />
                                  <h2>Metridiculis conseque quis</h2>
                                  <p>Orciinterdum condimenterdum nullamcorper elit nam curabitur laoreet met praesenean et
                                      iaculum. Metridiculis conseque quis iaculum aenean nunc aenean quis nam nis dui.</p>
                                  <p class="readmore"><a href="#">Read More Here &raquo;</a></p>
                              </li>
                              <li><img src="../static/img/demo/420x190.gif" alt="" />
                                  <h2>Metridiculis conseque quis</h2>
                                  <p>Orciinterdum condimenterdum nullamcorper elit nam curabitur laoreet met praesenean et
                                      iaculum. Metridiculis conseque quis iaculum aenean nunc aenean quis nam nis dui.</p>
                                  <p class="readmore"><a href="#">Read More Here &raquo;</a></p>
                              </li>
                              <li class="last"><img src="../static/img/demo/420x190.gif" alt="" />
                                  <h2>Metridiculis conseque quis</h2>
                                  <p>Orciinterdum condimenterdum nullamcorper elit nam curabitur laoreet met praesenean et
                                      iaculum. Metridiculis conseque quis iaculum aenean nunc aenean quis nam nis dui.</p>
                                  <p class="readmore"><a href="#">Read More Here &raquo;</a></p>
                              </li>
                              <li><img src="../static/img/demo/420x190.gif" alt="" />
                                  <h2>Metridiculis conseque quis</h2>
                                  <p>Orciinterdum condimenterdum nullamcorper elit nam curabitur laoreet met praesenean et
                                      iaculum. Metridiculis conseque quis iaculum aenean nunc aenean quis nam nis dui.</p>
                                  <p class="readmore"><a href="#">Read More Here &raquo;</a></p>
                              </li>
                              <li class="last"><img src="../static/img/demo/420x190.gif" alt="" />
                                  <h2>Metridiculis conseque quis</h2>
                                  <p>Orciinterdum condimenterdum nullamcorper elit nam curabitur laoreet met praesenean et
                                      iaculum. Metridiculis conseque quis iaculum aenean nunc aenean quis nam nis dui.</p>
                                  <p class="readmore"><a href="#">Read More Here &raquo;</a></p>
                              </li>
                          </ul>
                      </div>
                      {% endblock content %}
                      
                  </div>
              </div>
          </div>
          <!-- ####################################################################################################### -->
          <div class="wrapper row4">
              <div class="rnd">
                  <div id="footer" class="clear">
                      <!-- ####################################################################################################### -->
                      <div class="fl_left clear">
                          <!--高德地图链接-->
                          <div class="fl_left center"><img src="../static/img/demo/worldmap.gif" alt="" /><br />
                              <a
                                  href="https://www.amap.com/search?id=B00155HU50&city=310114&geoobj=121.447275%7C31.268923%7C121.458199%7C31.274481&query_type=IDQ&query=%E5%90%8C%E6%B5%8E%E5%A4%A7%E5%AD%A6%E5%98%89%E5%AE%9A%E6%A0%A1%E5%8C%BA&zoom=17.5">
                                  Find Us With AMap &raquo;</a></div>
                          <address>
                              Address Line 1: Tongji University<br />
                              Address Line 2: 4800, Cao'an Road, Huangdu Town, Jiading District<br />
                              City: Shanghai City<br />
                              Postcode: 200000<br />
                              <br />
                              Tel: (021)69589979<br />
                              Email: <a href="mailto:dxwg@tongji.edu.cn">dxwg@tongji.edu.cn</a>
                          </address>
                      </div>
                      <!-- ####################################################################################################### -->
                  </div>
              </div>
          </div>
          <!-- ####################################################################################################### -->
          </div>
      </body>
      
      </html>
      ```
  
  - [Beauty.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/Beauty.html)  ：模块网页
  
      ```jinja2
      {% extends 'Base.html' %}
      
      <!-- 这是一个用 jinja2 从Base.html渲染得到的实例 需要启动 flask 环境后才能看到-->
      <!-- 这样可以避免一项修改多处寻找 -->
      
      {% block title %}
          Beauty
      {% endblock title %}
      
      {% block content %}
      <div id="portfolio">
          <ul>
              {% for activity in item %}
              <li class="{{ loop.index0 | set_last_class_filter }}"><img src="{{activity.cover_image_path ~ activity.cover_image_name}}" alt="" />
                  <h2>{{activity.name}}</h2>
                  <p>{{activity.description}}</p>
                  <p class="readmore"><a href="{{'../' ~ activity.id}}">Read More Here &raquo;</a></p>
              </li>
              {% else %}
      <!--        如果没有该类活动，显示此处内容-->
              <h2>No Activity.</h2>
              {% endfor %}
          </ul>
      </div>
      {% endblock content %}
      ```
  
  - [Body.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/Body.html) ：模块网页
  
      ```jinja2
      {% extends 'Base.html' %}
      
      <!-- 这是一个用 jinja2 从Base.html渲染得到的实例 需要启动 flask 环境后才能看到-->
      <!-- 这样可以避免一项修改多处寻找 -->
      
      {% block title %}
          Body
      {% endblock title %}
      
      {% block content %}
      <div id="portfolio">
          <ul>
              {% for activity in item %}
                  <li class="{{ loop.index0 | set_last_class_filter }}"><img src="{{activity.cover_image_path ~ activity.cover_image_name}}" alt="" />
                  <h2>{{activity.name}}</h2>
                  <p>{{activity.description}}</p>
                  <p class="readmore"><a href="{{'../' ~ activity.id}}">Read More Here &raquo;</a></p>
              </li>
              {% else %}
              <!--如果没有该类活动，显示此处内容-->
              <h2>No Activity.</h2>
              {% endfor %}
          </ul>
      </div>
      {% endblock content %}
      ```
  
  - [Labor.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/Labor.html)   ：模块网页
  
      ```jinja2
      {% extends 'Base.html' %}
      
      <!-- 这是一个用 jinja2 从Base.html渲染得到的实例 需要启动 flask 环境后才能看到-->
      <!-- 这样可以避免一项修改多处寻找 -->
      
      {% block title %}
          Labor
      {% endblock title %}
      
      {% block content %}
      <div id="portfolio">
          <ul>
              {% for activity in item %}
              <li class="{{ loop.index0 | set_last_class_filter }}"><img src="{{activity.cover_image_path ~ activity.cover_image_name}}" alt="" />
                  <h2>{{activity.name}}</h2>
                  <p>{{activity.description}}</p>
                  <p class="readmore"><a href="{{'../' ~ activity.id}}">Read More Here &raquo;</a></p>
              </li>
              {% else %}
      <!--        如果没有该类活动，显示此处内容-->
              <h2>No Activity.</h2>
              {% endfor %}
          </ul>
      </div>
      {% endblock content %}
      ```
  
  - [Virtue.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/Virtue.html)   ：模块网页
  
      ```jinja2
      {% extends 'Base.html' %}
      
      <!-- 这是一个用 jinja2 从Base.html渲染得到的实例 需要启动 flask 环境后才能看到-->
      <!-- 这样可以避免一项修改多处寻找 -->
      
      {% block title %}
          Virtue
      {% endblock title %}
      
      {% block content %}
      <div id="portfolio">
          <ul>
              {% for activity in item %}
              <li class="{{ loop.index0 | set_last_class_filter }}"><img src="{{activity.cover_image_path ~ activity.cover_image_name}}" alt="" />
                  <h2>{{activity.name}}</h2>
                  <p>{{activity.description}}</p>
                  <p class="readmore"><a href="{{'../' ~ activity.id}}">Read More Here &raquo;</a></p>
              </li>
              {% else %}
      <!--        如果没有该类活动，显示此处内容-->
              <h2>No Activity.</h2>
              {% endfor %}
          </ul>
      </div>
      {% endblock content %}
      ```
  
  - [Wisdom.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/Wisdom.html)    ：模块网页
  
      ```jinja2
      {% extends 'Base.html' %}
      
      <!-- 这是一个用 jinja2 从Base.html渲染得到的实例 需要启动 flask 环境后才能看到-->
      <!-- 这样可以避免一项修改多处寻找 -->
      
      {% block title %}
          Wisdom
      {% endblock title %}
          
      {% block content %}
      <div id="portfolio">
          <ul>
              {% for activity in item %}
              <li class="{{ loop.index0 | set_last_class_filter }}"><img src="{{activity.cover_image_path ~ activity.cover_image_name}}" alt="" />
                  <h2>{{activity.name}}</h2>
                  <p>{{activity.description}}</p>
                  <p class="readmore"><a href="{{'../' ~ activity.id}}">Read More Here &raquo;</a></p>
              </li>
              {% else %}
      <!--        如果没有该类活动，显示此处内容-->
              <h2>No Activity.</h2>
              {% endfor %}
          </ul>
      </div>
      {% endblock content %}
      ```
  
  - [activity-demo.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/activity-demo.html)：活动展示网页
  
      ```jinja2
      {% extends 'Base.html' %}
      
      {% block title %}
        Activities
      {% endblock title %}
      
      {% block content %}
        <div class="wrapper row3">
          <div class="rnd">
            <div id="container" class="clear">
              <!-- ####################################################################################################### -->
              <h1>{{activity.name}}</h1>
              <p>{{activity.description}}</p>
              {% if operation == 'Apply' %}
              <a href="{{'../apply/' ~ act.id}}">Apply</a>
              {% elif operation == 'Abort' %}
              <a href="{{'../abort/' ~ act.id}}">Abort</a>
              {% elif operation == 'Delete' %}
              <a href="{{'../complete/' ~ act.id}}">Complete</a>
              <br>
              <br>
              <a href="{{'../delete/' ~ act.id}}">Delete</a>
              <br>
              <br>
              <a href="{{'../revise/' ~ act.id}}">Revise</a>
              {% else %}
      <!--        do nothing-->
              {% endif %}
              <img class="imgr" src="{{'.' ~ activity.cover_image_path ~ activity.cover_image_name}}" alt="" width="125" height="125" />
              <!-- ####################################################################################################### -->
            </div>
          </div>
        </div>
      {% endblock content %}
      ```
  
  - [index.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/index.html)：基本网页
  
      ```jinja2
      <!DOCTYPE html>
      <html>
      
      <head>
        <title>Second Classroom</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="imagetoolbar" content="no" />
        <link rel="stylesheet" href="../static/css/layout.css" type="text/css" />
      
        <!-- Homepage Specific Elements -->
        <script type="text/javascript" src="../static/js/jquery/jquery-1.4.1.min.js"></script>
        <script type="text/javascript" src="../static/js/jquery/jquery-ui-1.7.2.custom.min.js"></script>
        <script type="text/javascript" src="../static/js/jquery/jquery.tabs.setup.js"></script>
        <!-- End Homepage Specific Elements -->
      </head>
      
      <body id="top">
        <div class="wrapper row1">
          <div id="header" class="clear">
            <div class="fl_left">
              <h1><a href="index.html">Second Classroom</a></h1>
              <p>College of Electronics and Information Engineering</p>
            </div>
            <!--以下几个部分关于右上角，除Home外其他待修改-->
            <div class="fl_right">
              <ul>
                <li><a href={{url_for('home')}}>Home</a></li>
      					{% if g.userid %}
      					<li class="last">{{g.userid}}</li>
      					<li class="last"><a href={{url_for('auth.logout')}}>Logout Here</a></li>
      		  
      					{% else %}
      					<li class="last"><a href={{url_for('auth.login')}}>Login Here</a></li>
      					{%endif%}
              </ul>
              <form action="#" method="post" id="sitesearch">
                <fieldset>
                  <strong>Search:</strong>
                  <input type="text" value="Search Our Website&hellip;"
                    onfocus="this.value=(this.value=='Search Our Website&hellip;')? '' : this.value ;" />
                  <input type="image" src="../static/img/search.gif" id="search" alt="Search" />
                </fieldset>
              </form>
            </div>
          </div>
        </div>
        <!--以上部分为网页上端部分，各个网页关于上端部分应该相同，故修改上面部分仍何地方后要在wisdom,body等html文件中同步修改-->
        <!--五育页面格式相同，彼此也要同步修改-->
        <!-- ####################################################################################################### -->
        <!--以下为导航栏,导航栏遇到的问题是文字过于居中，应该令其两侧对齐，css文件在navi.css里topnav处-->
        <div class="wrapper row2">
          <div class="rnd">
            <!-- ###### -->
            <div id="topnav">
              <ul>
                <li><a href={{url_for('home')}}>Home</a></li>
                <li><a href={{url_for('module.virtue')}}>Morality Activity</a></li>
                <li><a href={{url_for('module.wisdom')}}>Wisdom Activity</a></li>
                <li><a href={{url_for('module.body_act')}}>Sports Activity</a></li>
                <li><a href={{url_for('module.beauty')}}>Arts Activity</a></li>
                <li><a href={{url_for('module.labor')}}>Labor Activity</a></li>
                <li class="last"><a href={{url_for('space.personal_page')}}>User Page</a></li>
                <!--个人建议将首页放在这里，但也有人提议放在其他地方-->
              </ul>
            </div>
            <!-- ###### -->
          </div>
        </div>
        <!-- ####################################################################################################### -->
        <div class="wrapper">
          <div id="featured_slide" class="clear">
            <!-- ###### -->
            <!--此处为上方图片右侧文字框，方案介绍待修改-->
            <!--注意，图片尺寸为950px * 250px,如果图片不是这个尺寸，拉伸后会变得很奇怪-->
            <!--此处为‘德’方案介绍-->
            <div class="overlay_left"></div>
            <div id="featured_content">
              <div class="featured_box" id="fc1"><img src="../static/img/1.jpg" alt="" />
                <div class="floater">
                  <h2>理想信念与价值观</h2>
                  <p>树立新时代青年人正确的人生观、价值观和世界观，有理想、有信仰。
                    明大德、守公德、立志报效祖国、服务人民、实现人生抱负，努力践行社会主义核心价值观。
                  </p>
                  <p class="readmore"><a href="{{url_for('module.virtue')}}">Continue Reading &raquo;</a></p>
                </div>
              </div>
              <!--此处为‘智’方案介绍-->
              <div class="featured_box" id="fc2"><img src="../static/img/2.jpg" alt="" />
                <div class="floater">
                  <h2>文化素养与能力提升</h2>
                  <p>选择性地研读古今中外的经典，养成爱读书、善读书的习惯；
                    培养谋求创新的意识和愿望，锻造实施创新的胆略和气魄；
                    知晓自我的专业兴趣和方向，努力提高学习能力、实践能力。
                  </p>
                  <br>
                  <p class="readmore"><a href="{{url_for('module.wisdom')}}">Continue Reading &raquo;</a></p>
                </div>
              </div>
              <!--此处为‘体’方案介绍-->
              <div class="featured_box" id="fc3"><img src="../static/img/3.jpg" alt="" />
                <div class="floater">
                  <h2>强身健体与意志培养</h2>
                  <p>学会合理自我认识，做到悦纳自己、情绪稳定、人际和谐、社会适应良好、培养乐观的心态和健全的人格、焕发青春美丽。树立健康的简直观念，主动参加体育锻炼，强健体魄、锤炼意志。</p>
                  <br>
                  <p class="readmore"><a href="{{url_for('module.body_act')}}">Continue Reading &raquo;</a></p>
                </div>
              </div>
              <!--此处为‘美’方案介绍-->
              <div class="featured_box" id="fc4"><img src="../static/img/4.jpg" alt="" />
                <div class="floater">
                  <h2>艺术鉴赏与审美实践</h2>
                  <p>树立正确而高尚的审美观，培养感知美、鉴赏美、创造美的审美能力，提升审美素养；以美辅德，以美启智，以美益体，以美助劳，陶冶道德情操，提升精神境界，完善人格塑造。</p>
                  <br>
                  <p class="readmore"><a href="{{url_for('module.beauty')}}">Continue Reading &raquo;</a></p>
                </div>
              </div>
              <!--此处为‘劳’方案介绍-->
              <div class="featured_box" id="fc5"><img src="../static/img/5.jpg" alt="" />
                <div class="floater">
                  <h2>劳动实践与志愿服务</h2>
                  <p>领悟劳动教育的新内涵，树立正确的劳动观，培养“淡泊名利，甘于奉献”的劳动平哥，进而提高劳动意愿、深化劳动情感、尊重劳动、劳动者和劳动果实，诚信劳动。</p>
                  <br>
                  <p class="readmore"><a href="{{url_for('module.labor')}}">Continue Reading &raquo;</a></p>
                </div>
              </div>
            </div>
            <!--此处为上方图片选择框的文字介绍部分，有文采的可以更改‘All About The...’的描述，但要超过四个单词-->
            <ul id="featured_tabs">
              <li><a href="#fc1">All About The Morality Activity</a></li>
              <li><a href="#fc2">All About The Wisdom Activity</a></li>
              <li><a href="#fc3">All About The Sports Activity</a></li>
              <li><a href="#fc4">All About The Arts Activity</a></li>
              <li class="last"><a href="#fc5">All About The Labor Activity</a></li>
            </ul>
            <div class="overlay_right"></div>
            <!-- ###### -->
          </div>
        </div>
        <!-- ####################################################################################################### -->
        <div class="wrapper row3">
          <div class="rnd">
            <div id="container" class="clear">
              <!-- ####################################################################################################### -->
              <!--这里是首页的介绍页面，建议从后端数据库提取活动放上来替换即可-->
              <div id="homepage" class="clear">
                <!-- ###### -->
                <div id="left_column">
                  <h2>Activities</h2>
                  <div class="imgholder"><img src="../static/img/001.jpg" alt="" width="220" height="90" /></a>
                  </div>
                  <!-- <h2>Current Students</h2> -->
                  <div class="imgholder"> <img src="../static/img/002.jpg" alt="" width="220" height="90" /></a></div>
                  <!-- <h2>Professors</h2> -->
                  <div class="imgholder"> <img src="../static/img/003.jpg" alt="" width="220" height="90"/></a></div>
                </div>
                <!-- ###### -->
                <div id="latestnews">
                  <h2>Recommended Events</h2>
                  <ul>
                    {% if item1 %}
                    <li class="clear">
                      <div class="imgl"><img src="{{item1.cover_image_path ~ item1.cover_image_name}}" alt="" width="125" height="125"/></div>
                      <div class="latestnews">
                        <p><a href="{{'../' ~ item1.id}}">{{item1.name}} &raquo;</a></p>
                        <p>{{item1.description}}</p>
                      </div>
                    </li>
                    {% else %}
                    {% endif %}
                    {% if item2 %}
                    <li class="clear">
                      <div class="imgl"><img src="{{item2.cover_image_path ~ item2.cover_image_name}}" alt="" width="125" height="125"/></div>
                      <div class="latestnews">
                        <p><a href="{{'../' ~ item2.id}}">{{item2.name}} &raquo;</a></p>
                        <p>{{item2.description}}</p>
                      </div>
                    </li>
                    {% else %}
                    {% endif %}
                    {% if item3 %}
                    <li class="clear">
                      <div class="imgl"><img src="{{item3.cover_image_path ~ item3.cover_image_name}}" alt="" width="125" height="125"/></div>
                      <div class="latestnews">
                        <p><a href="{{'../' ~ item3.id}}">{{item3.name}} &raquo;</a></p>
                        <p>{{item3.description}}</p>
                      </div>
                    </li>
                    {% else %}
                    {% endif %}
                  </ul>
                  <!--，祝你开心每一天！(bushi)-->
                  <p class="readmore">May you be happy every day!</a></p>
                </div>
                <!-- ###### -->
                <div id="right_column">
                  <div class="holder">
                    <h2>Activities</h2>
                    <div class="imgholder"> <img src="../static/img/004.jpg" alt="" width="220" height="90"/></a></div>
                    <div class="imgholder"> <img src="../static/img/005.jpg" alt="" width="220" height="90"/></a></div>
                    <div class="imgholder"> <img src="../static/img/006.jpg" alt="" width="220" height="90"/></a></div>
                  </div>
                  <div class="holder">
                    <h2>Quick Information</h2>
                    <div class="apply"><a href={{url_for('auth.login')}}><img src="../static/img/13.jpg" alt="" />
                        <strong>Make A Quick
                          Login</strong></a>
                    </div>
                  </div>
                </div>
                <!-- ###### -->
              </div>
              <!-- ####################################################################################################### -->
              <div id="twitter" class="clear">
                <!--homepage.css 中twitter.fl_left中有twitter的logo，我注释掉了，有能者可以替换成同色背景，相同大小的同济logo-->
                <div class="fl_left"><a href="https://see.tongji.edu.cn/">Follow Us On CEIE</a></div>
                <div class="fl_right">
                  我仰望星空，
                  它是那样壮丽而光辉；<br>
                  那永恒的炽热，
                  让我心中燃起希望的烈焰、响起春雷。
                </div>
              </div>
              <!-- ####################################################################################################### -->
            </div>
          </div>
        </div>
        <!-- ####################################################################################################### -->
        <div class="wrapper row4">
          <div class="rnd">
            <div id="footer" class="clear">
              <!-- ####################################################################################################### -->
              <div class="fl_left clear">
                <!--高德地图链接-->
                <div class="fl_left center"><img src="../static/img/demo/worldmap.gif" alt="" /><br />
                  <a
                    href="https://www.amap.com/search?id=B00155HU50&city=310114&geoobj=121.447275%7C31.268923%7C121.458199%7C31.274481&query_type=IDQ&query=%E5%90%8C%E6%B5%8E%E5%A4%A7%E5%AD%A6%E5%98%89%E5%AE%9A%E6%A0%A1%E5%8C%BA&zoom=17.5">
                    Find Us With AMap &raquo;</a>
                </div>
                <address>
                  Address Line 1: Tongji University<br />
                  Address Line 2: 4800, Cao'an Road, Huangdu Town, Jiading District<br />
                  City: Shanghai City<br />
                  Postcode: 200000<br />
                  <br />
                  Tel: (021)69589979<br />
                  Email: <a href="mailto:dxwg@tongji.edu.cn">dxwg@tongji.edu.cn</a>
                </address>
              </div>
              <!-- ####################################################################################################### -->
            </div>
          </div>
        </div>
        <!-- ####################################################################################################### -->
        </div>
      </body>
      
      </html>
      ```
  
  - [login.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/login.html) ：登录网页
  
      ```jinja2
      <!-----------------------
      Name: login.html
      Function: 用户登录界面
      Author: king
      Status: continue
      ------------------------>
      
      <!DOCTYPE HTML>
      <html lang="en">
      <html>
      
      <head>
          <title>Login</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta charset="utf-8">
          <link rel="stylesheet" type="text/css" href="../static/css/login_style.css">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
          <link href='https://fonts.googleapis.com/css?family=Titillium+Web:400,300,600' rel='stylesheet' type='text/css'>
          <link href='https://fonts.googleapis.com/css?family=Titillium+Web:400,300,600' rel='stylesheet' type='text/css'>
          <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      </head>
      <script src="../static/js/SakuraFall.js"></script>
      
      <body class="body">
      
          <div class="login-page">
              <div class="form">
      
                  <form action="{{ url_for('auth.login') }}" method="POST">
                      <lottie-player src="../static/json/login.json" background="transparent" speed="1"
                          style="justify-content: center;" loop autoplay></lottie-player>
                          {{text}}        <!--此处为信息反馈，比如错误信息反馈-->
                      <input type="text" placeholder="&#xf007;  username" name="userid" oninput="value=value.replace(/[^\d]/g,'')"
                          maxlength="8" />
                      <input type="password" placeholder="&#xf023;  password" name="password" maxlength="30" />
                      <button>LOGIN</button>
                      <p class="message"></p>
                  </form>
      
                  <form class="login-form">
                      <a href={{url_for("auth.regist")}}>
                      <button type="button">REGISTER</button>
                      </a>
                  </form>
              </div>
          </div>
      
      </body>
      
      </html>
      ```
  
  - [signup.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/signup.html) ：注册网页
  
      ```jinja2
      <!-----------------------------
      Name: signup
      Function: 网站的用户注册界面
      Author: king
      ------------------------------>
      <!DOCTYPE HTML>
      <html lang="en" >
      <html>
      <head>
        <title>Sign Up</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="utf-8">
        <link rel="stylesheet" type="text/css" href="../static/css/signup_style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link href='https://fonts.googleapis.com/css?family=Titillium+Web:400,300,600' rel='stylesheet' type='text/css'>  
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
      </head>
      <script src="../static/js/SakuraFall.js"></script>
      
      <body class="body">
        
      <div class="login-page">
        <div class="form">
          <form action="{{ url_for('auth.regist') }}" method="POST">
            <lottie-player src="../static/json/signup.json"  background="transparent"  speed="1"  style="justify-content: center;" loop  autoplay></lottie-player>
            {{text}}
            <input type="text" placeholder="username" name="userid" oninput="value=value.replace(/[^\d]/g,'')" maxlength="8"/>
            <!--input type="text" placeholder="email address"/>
            <input type="text" placeholder="pick a username"/-->
            <input type="password" placeholder="password" name="password" maxlength="30"/>
            <input type="password" placeholder="password again" name="password2" maxlength="30"/>
      
            <select name="identity" type="password" class="selected" style="left:10%; font-size: 15px;">
                <option value="student" selected="" style="left:10px; font-size: 15px; font-family:'New York';">  Student</option>
                <option value="teacher" style="left:10px; font-size: 15px; font-family:'New York';">  Teacher</option>
            </select>
      
            <br><br>
            <button>REGISTER</button>
            <p class="message"></p>
            
          </form>
      
          <form class="login-form">
            
          </form>
        </div>
      </div>
      
      </body>
      </html>
      ```
  
  - [user.html](https://github.com/yuanyangwangTJ/website/blob/master/templates/user.html) ：用户主页
  
      ```jinja2
      <!-----------------------
      Name: user.html
      Function: 个人用户界面
      Author: king
      ------------------------>
      
      <!DOCTYPE html>
      <html>
      
      <head>
      	<!-- Basic Page Info -->
      	<meta charset="utf-8">
      	{% block header %}
      	<title>Personal Data</title>
      	{% endblock header %}
      
      	<!-- Mobile Specific Metas -->
      	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
      	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      	<meta http-equiv="imagetoolbar" content="no" />
      
      	<!-- CSS -->
      	<link rel="stylesheet" type="text/css" href="../static/css/style.css">
      	<link rel="stylesheet" type="text/css" href="../static/styles/core.css">     
      	<link rel="stylesheet" type="text/css" href="../static/styles/icon-font.min.css">
      	<link rel="stylesheet" type="text/css" href="../static/styles/style.css">     
      	<link rel="stylesheet" href="../static/css/layout.css" type="text/css" />
      
      	<!--Get time-->
      	<script>
      		window.dataLayer = window.dataLayer || [];
      		function gtag() { dataLayer.push(arguments); }
      		gtag('js', new Date());
      		gtag('config', 'UA-119386393-1');
      	</script>
      </head>
      <!-- ####################################################################################################### -->
      
      <body id="top">
      	<div class="wrapper row1">
      		<div id="header" class="clear">
      			<div class="fl_left">
      				<h1><a href="index.html">Second Classroom</a></h1>
      				<p>College of Electronics and Information Engineering</p>
      			</div>
      			<!--以下几个部分关于右上角，除Home外其他待修改-->
      			<div class="fl_right">
      				<ul>
      					<li><a href="index.html">Home</a></li>
      					<li><a href="#">Contact Us</a></li>
      					<li><a href="#">A - Z Index</a></li>
      					<li><a href="#">Student Login</a></li>
      					<li class="last"><a href="#">Staff Login</a></li>
      				</ul>
      				<form action="#" method="post" id="sitesearch">
      					<fieldset>
      						<strong>Search:</strong>
      						<input type="text" value="Search Our Website&hellip;"
      							onfocus="this.value=(this.value=='Search Our Website&hellip;')? '' : this.value ;" />
      						<input type="image" src="../static/img/search.gif" id="search" alt="Search" />
      					</fieldset>
      				</form>
      			</div>
      		</div>
      	</div>
      	<!--以上部分为网页上端部分，各个网页关于上端部分应该相同，故修改上面部分仍何地方后要在wisdom,body等html文件中同步修改-->
      	<!--五育页面格式相同，彼此也要同步修改-->
      	<!-- ####################################################################################################### -->
      	<!--以下为导航栏,导航栏遇到的问题是文字过于居中，应该令其两侧对齐，css文件在navi.css里topnav处-->
      	<div class="wrapper row2">
      		<div class="rnd">
      			<!-- ###### -->
      			<div id="topnav">
      				<ul>
      					<li><a href="index.html">Home</a></li>
      					<li><a href="Virtue.html">Virtue Activity</a></li>
      					<li><a href="Wisdom.html">Wisdom Activity</a></li>
      					<li><a href="Body.html">Body Activity</a></li>
      					<li><a href="Beauty.html">Beauty Activity</a></li>
      					<li><a href="Labor.html">Labor Activity</a></li>
      					<li class="active" class="last"><a href="user.html">User Page</a></li>
      					<!--个人建议将首页放在这里，但也有人提议放在其他地方-->
      				</ul>
      			</div>
      			<!-- ###### -->
      		</div>
      	</div>
      	<!-- ####################################################################################################### -->
      	<!--日历小挂件-->
      	<div class="canlenda">
      		<div class="col-md-4 col-sm-12 text-center">
      			<div class="mb-20">
      				<div class="datepicker-here" data-timepicker="true" data-language='en'></div>
      			</div>
      		</div>
      	</div>
      
      	<!--主体内容，显示德育分数-->
      	<!--begin main-container-->
      	<div class="mobile-menu-overlay"></div>
      	<div class="main-container">
      		<div class="xs-pd-20-10 pd-ltr-20">
      			<div class="page-header">
      				<div class="row">
      					<div class="col-md-6 col-sm-12">
      						<div class="title">
      							<h4>Your Score</h4>
      						</div>
      						<nav aria-label="breadcrumb" role="navigation">
      							<ol class="breadcrumb">
      								<li class="breadcrumb-item"><a href="index.html">Home</a></li>
      								<li class="breadcrumb-item active" aria-current="page">Your Score</li>
      							</ol>
      						</nav>
      					</div>
      
      					<!--在此处显示时间-->
      					<div class="col-md-6 col-sm-12 text-right">
      						<div class="dropdown">
      							<a class="btn btn-primary dropdown-toggle" href="#" role="button" data-toggle="dropdown">
      								December 2020
      							</a>
      						</div>
      					</div>
      				</div>
      			</div>
      
      			{% block content %}
      
      			<div class="row clearfix progress-box">
      				<!--本行的作用为保证各个模块横排-->
      
      				<!--显示各个模块的分数，注意接口的分数以及百分比的计算-->
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-blue padding-top-10 h5">Virtue Score</h5>
      							<span class="d-block">80% Average <i class="fa fa-line-chart text-blue"></i></span>
      						</div>
      					</div>
      				</div>
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-green padding-top-10 h5">Wisdom Score</h5>
      							<span class="d-block">75% Average <i class="fa text-light-green fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-orange padding-top-10 h5">Body Score</h5>
      							<span class="d-block">90% Average <i class="fa text-light-orange fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-purple padding-top-10 h5">Beauty Score</h5>
      							<span class="d-block">65% Average <i class="fa text-light-purple fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-blue padding-top-10 h5">Labor Score</h5>
      							<span class="d-block">80% Average <i class="fa fa-line-chart text-blue"></i></span>
      						</div>
      					</div>
      				</div>
      
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-purple padding-top-10 h5">Total Score</h5>
      							<span class="d-block">65% Average <i class="fa text-light-purple fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      
      				<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
      					<div class="card-box pd-30 height-100-p">
      						<div class="progress-box text-center">
      							<h5 class="text-light-orange padding-top-10 h5">Rest Score</h5>
      							<span class="d-block">35% Average <i class="fa text-light-orange fa-line-chart"></i></span>
      						</div>
      					</div>
      				</div>
      			</div>
      			{% endblock content %}
      
      			<!-- ####################################################################################################### -->
      			<!--此处用来打表，将该名用户报名活动输出出来-->
      			<div class="page-header">
      
      				<div class="row">
      					<div class="col-md-6 col-sm-12">
      						<h4>此处用来打表，将该名用户报名活动输出出来</h4>
      					</div>
      				</div>
      			</div>
      			<!-- ####################################################################################################### -->
      			<div class="wrapper row4">
      				<div class="rnd">
      					<div id="footer" class="clear">
      						<!-- ####################################################################################################### -->
      						<div class="fl_left clear">
      							<!--高德地图链接-->
      							<div class="fl_left center"><img src="../static/img/demo/worldmap.gif" alt="" /><br />
      								<a
      									href="https://www.amap.com/search?id=B00155HU50&city=310114&geoobj=121.447275%7C31.268923%7C121.458199%7C31.274481&query_type=IDQ&query=%E5%90%8C%E6%B5%8E%E5%A4%A7%E5%AD%A6%E5%98%89%E5%AE%9A%E6%A0%A1%E5%8C%BA&zoom=17.5">
      									Find Us With AMap &raquo;</a>
      							</div>
      							<address>
      								Address Line 1: Tongji University<br />
      								Address Line 2: 4800, Cao'an Road, Huangdu Town, Jiading District<br />
      								City: Shanghai City<br />
      								Postcode: 200000<br />
      								<br />
      								Tel: (021)69589979<br />
      								Email: <a href="mailto:dxwg@tongji.edu.cn">dxwg@tongji.edu.cn</a>
      							</address>
      						</div>
      						<!-- ####################################################################################################### -->
      					</div>
      				</div>
      			</div>
      			<!-- ####################################################################################################### -->
      		</div>
      	</div>
      	
      	<!-- js -->
      	<!--日历启动的核心js-->
      	<script src="../static/scripts/core.js"></script>
      
      </body>
      
      </html>
      ```
  
* CSS

因为篇幅原因，只列举出部分，具体内容可见[**Github仓库**](https://github.com/yuanyangwangTJ/website.git)

 **`style.css`**

```css
body {
    background-color: #ddf0e4;
    background-image: linear-gradient(to right, #8edce0, #ddf0e4, #ddf0e4,  #ddf0e4);
}

/*定义左侧导航栏的样式*/

.ul-left {
    list-style-type: none;
    margin: 0 30px 0 30px;
    padding: 20px;
    width: 10%;
    top: 10%;
    background-color: #f6f4f0;
    position: fixed;
    height: 80%;
    overflow: auto;
    border-radius: 10px;
    box-shadow: 10px 10px 5px gray;
}

.li-left a {
    display: block;
    color: #000;
    margin: 20px 10px;
    border-radius: 5px;
    
    padding: 8px 16px;
    font-size: 15px;
    font-family: fantasy;
    font-weight:bold;
    text-decoration: none;
    text-align: center;
}

.li-left a.active {
    background-color: #01bbb0;
    box-shadow: 5px 5px 3px gray;
    color: white;
}

.li-left a:hover:not(.active) {
    background-color: #555;
    color: white;
    box-shadow: 5px 5px 3px gray;
}

/*日历样式编辑*/
.canlenda {
    width: 250px;
    height: auto;
    float: left;
    margin: 23px auto;
    position: fixed;
}

.canlenda2 {
    width: 250px;
    height: auto;
    top: 20%;
    right: 5px;
    float: right;
    margin: 3px auto;
    
}

/*文本提交框*/
.file-submit {
    height: auto;
    width: 800px;
    top: 40%;
    left: 1.5%;
    position: relative;
}

/*活动模块选择*/
.activity-select {
    border-collapse: black;
    border-radius: 3px;
    width:210px;
    height: 40px;
    font-weight: bold;
}

/*活动发布排版*/
.public-activity {
    margin: 10px 25px 20px;  
}
```

**` table.css `**

```css
/*
Template Name: Academic Education
File: Tables CSS
Author: OS Templates
Author URI: http://www.cssmoban.com/
Licence: <a href="#">Website Template Licence</a>
*/

table{
	width:100%;
	border-collapse:collapse;
	table-layout:auto;
	vertical-align:top;
	margin-bottom:15px;
	border:1px solid #CCCCCC;
	}

table thead th{
	color:#FFFFFF;
	background-color:#06213F;
	border:1px solid #CCCCCC;
	border-collapse:collapse;
	text-align:center;
	table-layout:auto;
	vertical-align:middle;
	}

table tbody td{
	vertical-align:top;
	border-collapse:collapse;
	border-left:1px solid #CCCCCC;
	border-right:1px solid #CCCCCC;
	}
	
table thead th, table tbody td{
	padding:5px;
	border-collapse:collapse;
	}

table tbody tr.light{
	color:#666666;
	background-color:#F7F7F7;
	}

table tbody tr.dark{
	color:#666666;
	background-color:#E8E8E8;
	}
```

**`signup.css`**

```css
@import url('../webix/login_signup_webix.css');

.body{
  background-image: url('../img/background02.png');
  background-repeat: no-repeat;
  background-size: cover;
}

.selected {
  padding: 5px 0;
  border-radius: 10px;
  width: 270px;
  height: 45px;
  font-size: large;
  color: #0b0f40;
}

.login-page {
  width: 360px;
  padding: 8% 0 0;
  margin: auto;

}
.form {
  position: relative;
  z-index: 1;
  background: rgba(145,191,188,0.4);
  max-width: 360px;
  margin: 0 auto 100px;
  padding: 45px;
  text-align: center;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
  
}
.form input {
  font-family: FontAwesome, "Roboto", sans-serif;
  outline: 0;
  background: #f2f2f2;
  width: 100%;
  border: 0;
  margin: 0 0 15px;
  padding: 15px;
  box-sizing: border-box;
  font-size: 14px;
border-radius:10px;
  
}
.form button {
  font-family: "Titillium Web", sans-serif;
  font-size: 14px;
  font-weight: bold;
  letter-spacing: .1em;
  outline: 0;
  background: #17a589;
  width: 100%;
  border: 0;
border-radius:30px;
  margin: 0px 0px 8px;
  padding: 15px;
  color: #FFFFFF;
  -webkit-transition: all 0.3 ease;
  transition: all 0.3 ease;
  cursor: pointer;
  transition: all 0.2s;

}
.form button:hover,.form button:focus {
  background: #148f77;
   box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  transform: translateY(-4px);
}
.form button:active {
  transform: translateY(2px);
  box-shadow: 0 2.5px 5px rgba(0, 0, 0, 0.2);
}

.form .message {
  
  margin: 6px 6px;
  color: #808080;
  font-size: 11px;
  text-align: center;
  font-weight: bold;
  font-style: normal;

  

}
.form .message a {
  color: #FFFFFF;
  text-decoration: none;
  font-size: 13px;
}
.form .register-form {
  display: none;
}
.container {
  position: relative;
  z-index: 1;
  max-width: 300px;
  margin: 0 auto;
}
.container:before, .container:after {
  content: "";
  display: block;
  clear: both;
}
.container .info {
  margin: 50px auto;
  text-align: center;
}
.container .info h1 {
  margin: 0 0 15px;
  padding: 0;
  font-size: 36px;
  font-weight: 300;
  color: #1a1a1a;
}
.container .info span {
  color: #4d4d4d;
  font-size: 12px;
}
.container .info span a {
  color: #000000;
  text-decoration: none;
}
.container .info span .fa {
  color: #EF3B3A;
}
body {
  background: #76b852; /* fallback for old browsers */
  background: -webkit-linear-gradient(right, #76b852, #8DC26F);
  background: -moz-linear-gradient(right, #76b852, #8DC26F);
  background: -o-linear-gradient(right, #76b852, #8DC26F);
  background: linear-gradient(to left, #76b852, #8DC26F);
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;    
}

```

**更多文件以及样式详见[Github仓库](https://github.com/yuanyangwangTJ/website.git)**.

****

### 项目图片

项目图片上传至图床（链接如下），也可以在[Github仓库](https://github.com/yuanyangwangTJ/website.git)查看.

[Picture1](https://s3.ax1x.com/2020/12/23/r6QJ56.jpg)
[Picture2](https://s3.ax1x.com/2020/12/23/r6QN8O.jpg)
[Picture3](https://s3.ax1x.com/2020/12/23/r6QGUx.jpg)
[Picture4](https://s3.ax1x.com/2020/12/23/r6Q2RS.jpg)
[Picture5](https://s3.ax1x.com/2020/12/23/r6Q8V1.jpg)
[Picture6](https://s3.ax1x.com/2020/12/23/r6QRxg.jpg)
[Picture7](https://s3.ax1x.com/2020/12/23/r6QtPK.jpg)
[Picture8](https://s3.ax1x.com/2020/12/23/r6QfMQ.jpg)
[Picture9](https://s3.ax1x.com/2020/12/23/r6QU2D.jpg)
[Picture10](https://s3.ax1x.com/2020/12/23/r6Qaxe.jpg)
[Picture11](https://s3.ax1x.com/2020/12/23/r6QwKH.jpg)
[Picture12](https://s3.ax1x.com/2020/12/23/r6Q0rd.jpg)
[Picture13](https://s3.ax1x.com/2020/12/23/r6QBqA.jpg)
[Picture14](https://s3.ax1x.com/2020/12/23/r6QrVI.jpg)
[Picture15](https://s3.ax1x.com/2020/12/23/r6Qsat.jpg)
[Picture16](https://s3.ax1x.com/2020/12/23/r6QyIP.jpg)
[Picture17](https://s3.ax1x.com/2020/12/23/r6QcPf.jpg)
[Picture18](https://s3.ax1x.com/2020/12/23/r6QgG8.jpg)
[Picture19](https://s3.ax1x.com/2020/12/23/r6Q4qs.jpg)
[Picture20](https://s3.ax1x.com/2020/12/23/r6Qhrj.jpg)
[Picture21](https://s3.ax1x.com/2020/12/23/r6QbGT.jpg)
[Picture22](https://s3.ax1x.com/2020/12/23/r6QTI0.jpg)
[Picture23](https://s3.ax1x.com/2020/12/23/r6QHiV.gif)
[Picture24](https://s3.ax1x.com/2020/12/23/r6QvL9.jpg)
[Picture25](https://s3.ax1x.com/2020/12/23/r6QLzF.gif)
[Picture26](https://s3.ax1x.com/2020/12/23/r6QXM4.jpg)
[Picture27](https://s3.ax1x.com/2020/12/23/r6QjsJ.jpg)
[Picture28](https://s3.ax1x.com/2020/12/23/r6QzZR.png)
[Picture29](https://s3.ax1x.com/2020/12/23/r6lSd1.png)
[Picture30](https://s3.ax1x.com/2020/12/23/r6lpIx.png)
[Picture31](https://s3.ax1x.com/2020/12/23/r6lCi6.gif)

****

## 8. 网站演示效果图

### 1. 登录

<img src="C:\Users\86152\AppData\Roaming\Typora\typora-user-images\image-20201223165440617.png" alt="image-20201223165440617" style="zoom:80%;" />

### 2. 教师发布首页

<img src="C:\Users\86152\AppData\Roaming\Typora\typora-user-images\image-20201223165640490.png" alt="image-20201223165640490" style="zoom:80%;" />

### 3. 网站首页

<img src="C:\Users\86152\AppData\Roaming\Typora\typora-user-images\image-20201223165904494.png" alt="image-20201223165904494" style="zoom:80%;" />

**因为空间限制，仅展示部分图片以供参考**

****

## 9. 声明

**免责声明：**网站为计算机科学导论课程网页设计作业，并不用于其他用途.			

——**计算机科学导论第五小组**

****