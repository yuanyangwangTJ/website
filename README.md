# website

## 0. 网站样式演示

* **Home**

![avatar](./website-demo/Home.png)

****

* **login**

![avatar](./website-demo/login.png)

****

* **register**

![avatar](./website-demo/register.png)

****

* **teacher**

![avatar](./website-demo/teacher.png)

****

* **student**

![avatar](./website-demo/student.png)

****

**更多内容请登录网站查看**

****



## 1.网站功能介绍

实现第二课堂功能的网站，实现第二课堂的计分、查看等功能。分为教师和学生身份登录，其中学生可以注册账号，教师账号由后台设置。下面就网站的具体功能罗列如下：
### 网站模块功能(wyy编)
* **登录/注册功能**
  
  > **学生教师**的统一登录界面，学生账号的注册界面
  >
  > 关于**头像**功能：用户初始登录时由网站默认分配头像，用户可以使用更改头像的功能上传头像图片并保存。（此功能根据实现过程选择保留与否）

* **德育模块**
  
  > **德：理想信念与核心价值观**
  >
  > **智：文化素养与能力提升**
  >
  > **体：强身健体与意志培养**
  >
  > **美：艺术鉴赏与审美实践**
  >
  > **劳：劳动实践与志愿服务**

* **德育分数**

  > **学生**：为学生提供提交的活动模块下的活动的选择，提供书写感受的文本框，提交。
  >
  > **教师**：教师端收到学生的提交选择审核是否通过，并由系统反馈给学生是否通过的信息。
  >
  > 以上过程完成，计入学生德育分数
  > 
  
* **日历表功能**

  - **学生可以通过点击日历表查看所选时期是否有活动**
  
* **首页推送**

  - **及时推送一些德育活动**
  
* **其他功能**
  
  >私信辅导员
  >
  >匿名评论
  >
  >群聊

**欢迎添加自己的建议或者可实现功能！！！**

**以上所有功能根据在实现过程中的操作可行性及时调整**

### 设计(qzl编)

- 页面逻辑
	1. 主界面
		- 展示活动列表，与部分活动信息
		- 也可以考虑分栏目显示
		- 对于未登录和已经登录应有不同的表现
			- 未登录要提供登录入口
			- 登录后提供头像等显示应有发布、删除活动的功能
			- 对于管理员
	2. 登录/注册的界面
		- 通过POST向后端传送注册/登录信息
		- 如果注册/登录失败，后端传回反馈
		- 注册后无需登录，直接进入主界面
	3. 活动详情页
		- 包含各种活动信息
		- 对于教师有修改信息的权力
		- 教师也可以在这一页审核学生的报名情况
		- 学生可以在这一页报名活动、查看自己的报名情况
	4. 个人页面
		- 展示已报名活动
		- 展示审核通过活动
		- 展示已参与并结束的活动
	5. 活动发布页
		- 这一页只有教师能够登入
		- 有发布活动的功能
- 数据库
	- 用户登录信息表
		- id
		- 账户类型 （学生或管理员）
		- 头像
		- 密码（加密后）
	- 用户报名活动表
		- id
		- 已经申请的活动（同上）
		- 已报名的活动（xml？）
		- 未通过申请的活动
	- 用户系统消息表（？）
		- id
		- 消息表（xml?）
	- 活动表
		- id
		- 封面图（？）
		- 类型（五个模块）
		- 活动名称
		- 活动介绍
		- 各种时间
		- 报名学生（xml，包括通过与未通过）

## 2.前端

### 负责人员

* 王远洋，王嘉俊，王麒斌
### 实现界面

* 用户登录以及注册界面
* 用户消息、通知的功能
* 用户更改头像的界面
* 用户查看日历的界面
* 用户提交德育活动的界面
* 教师审核的界面
* 学生和教师的主界面

### 学习参考网站

web前端需要`HTML, CSS, Javascript`的知识储备，下面将一些学习网站分享如下**（若有较好的推荐网站，可以分享到这里供大家学习参考）**

1. **HTML**

   [**mozilla基金会HTML详解（最全面）**](https://developer.mozilla.org/zh-CN/docs/Web/HTML)

   [**菜鸟教程HTML（通俗性强）**](https://www.runoob.com/html/html-tutorial.html)

   [**网站模板**](https://www.liaoxuefeng.com/wiki/897692888725344/923057271077472)

2. **CSS**

   同上面，**Mozilla以及菜鸟教程**


3. **JavaScript**

   同上

   [**廖雪峰JavaScript教程**](https://www.liaoxuefeng.com/wiki/1022910821149312)

4. **Bootstrap框架**

   [**Bootstrap中文手册**](https://v3.bootcss.com/css/#type-transformation)

   [**菜鸟教程Bootstrap**](https://www.runoob.com/bootstrap/bootstrap-tutorial.html)

5. **jQuery框架**

   [**菜鸟教程jQuery**](https://www.runoob.com/jquery/jquery-tutorial.html)

6. **更多分享，欢迎添加**

7. **Flask**

   [**Flask前后端连接示例**](https://zhuanlan.zhihu.com/p/104273184)

​    

## 3. 后端

### **负责人员**

- 裘自立，徐佳春，韩孟霖

### 学习参考网站

后端按要求需要使用 `Flask`及`Mysql`，若要复用`html`页面还需要了解`Jinja2`模板引擎。

数据库还可以自由选用`Flask`中文文档推荐使用的`python`内置的`sqlite3`。

1. **Flask**

    [**Flask中文文档**](https://dormousehole.readthedocs.io/en/latest/)

2.  **MySQL**

   [**MySQL菜鸟教程**](https://www.runoob.com/mysql/mysql-tutorial.html) （注：版本较老，部分指令实测无法在8.0版本运行）

   [**MySQL官方文档**](https://dev.mysql.com/doc/) 

3. **SQLite**

   [**SQLite菜鸟教程**](https://www.runoob.com/sqlite/sqlite-tutorial.html) 

4. **Jinja**

   [**Jinja官方文档**](https://jinja.palletsprojects.com/en/2.11.x/) 

   [**Jinja2中文手册**](http://www.ainoob.cn/docs/jinja2/intro.html)

5. [**腾讯开发者手册**](https://cloud.tencent.com/developer/devdocs)