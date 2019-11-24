# charset=utf8
from flask import Flask, request, jsonify
from flask_login import logout_user
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

# 初始化
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ZHBzhb123123@112.124.26.56/User"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class UsersModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256))

    def userdata(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password
        }


db.create_all()


# 用户登录
@app.route('/users/<int:id_>', methods=["GET"])
def getuser(id_):
    user = UsersModel.query.get(id_)
    if not user:
        return jsonify({
            "status": 2,
            "message": "此用户不存在",
        })
    data = user.userdata()
    return jsonify({
        "status": 1,
        "message": "获取信息成功",
        "data": data
    })


@app.route('/users', methods=["GET"])
def getdata():
    users = UsersModel.query.all()
    data = [user.userdata() for user in users]
    return jsonify({
        "status": 1,
        "message": "获取成功",
        "data": data
    })


# 用户注册
@app.route('/users/signup', methods=["POST"])
def signup():
    data = {
        "name": request.json.get("name"),
        "password": request.json.get("password"),
        "id": request.json.get("id")
    }
    user = UsersModel(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "操作成功"
    })


# 用户退出
@app.route('/logout')
def logout():
    logout_user()
    return jsonify({
        "status": 1,
        "message": "操作成功"
    })




if __name__ == '__main__':
    app.run()
