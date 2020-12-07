#-------------------------------------
# Name: debug
# Function: 前端调试界面的运行代码
# PS: 本代码为调试代码，后端无需使用修改
#-------------------------------------

from flask import  Flask,render_template
app = Flask(__name__)

@app.route('/')
def base():
    msg = "my name is caojianhua, China up!"
    return render_template("index.html", data=msg)  #加入变量传递

if __name__=="__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)