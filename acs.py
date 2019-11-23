from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
#app.config[SQLAlchemy_DATABASE_URL] = "mysql+pymysql://root:20020624jjj@localhost/activities?charset=utf8"

#db = SQLAlchemy(app)
#用户输入，录入数据库表单
create_table = """CREATE TABLE acs(
        act text,
        name varchar(100),
        place text,
        deadline varchar(100),
        PRIMARY KEY (name)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    #连接数据库
connect = pymysql.connect(host = 'localhost',user = 'root',password = '20020624jjj',db = 'activities',port = 3306,charset = 'utf8')

cursor = connect.cursor()
cursor.execute(create_table)#创建表单

cursor.close()
connect.close()
db.close()
