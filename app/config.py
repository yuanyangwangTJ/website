#flask
DEBUG = True
#session
SECRET_KEY="1145141919810"

#mysql
DIQLECT = "mysql"
DRIVER="pymysql"
USERNAME = "root"
# PASSWORD = "root"
PASSWORD = "root"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "CSBIGHW"


SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIQLECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS =False
