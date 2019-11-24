from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import  pprint
import  json


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:20020624jjj@localhost/activities?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
#用户输入，录入数据库表单.
#创建表单，存放用户输入数据.

class CreateTable(db.Model):
    __tablename__='acs'
    id = db.Column(db.String(16),primary_key=True,unique=True)
    act = db.Column(db.Text)
    name = db.Column(db.String(64))
    place = db.Column(db.Text)
    data = db.Column(db.String(64))

db.create_all()

#将获取内容输入到表单中

#从前端获取json数据，装换为字典

@app.route('/',methods=['GET'])
def GetContent():

    connect = pymysql.connect(host='localhost', user='root', password='20020624jjj', db='activities', port=3306,charset='utf8')
    cursor = connect.cursor()
    sql = """INSERT INTO acs(id, act,name,place,data)VALUES(*,*,*,*,*)"""#*占位
    cursor.execute(sql)
    connect.commit()
    try:
        cursor.close()
        connect.close()
    except:
        db.rollback()
    db.close()


#从表单中得到数据并展示
@app.route('/',methods=['POST'])
def ShowContent():
    connect = pymysql.connect(host='localhost', user='root', password='20020624jjj', db='activities', port=3306,charset='utf8')
    find = """SELECT *FROM acs"""
    cursor = connect.cursor()
    cursor.execute(find)
    result = cursor.fetchall()
    pprint.pprint(result)
    para = []
    for i in result:
        text = {'id':i[0],'活动':i[1],'邀请人':i[2],'地点':i[3],'时间':i[4]}
        para.append(text)
        return json.dumps(para, ensure_ascii=False, indent=4)


if __name__ =='__main__':
    app.run(debug=True)