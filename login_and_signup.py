# charset=utf8
from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_login import logout_user
from functools import wraps
from sqlalchemy import and_
from flask_sqlalchemy import SQLAlchemy

# 初始化
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sql+mysql://root:ZHBzhb123123@localhost"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "Students"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80))

    def __init__(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

    db.create_all()


# 错误信息显示
@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404


# 登录
def valid_login(username, password):
    users = User.query.filter(and_(User.username == username, User.password == password)).first()
    if users:
        return jsonify({
            "status": 1,
            "message": "获取成功"

        })
    else:
        return jsonify({
            "status": 2,
            "message": "获取失败"
        })


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))

    return wrapper


@app.route('/login', method=["get"])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form.get('username')
            return jsonify({
                "status": 1,
                "message": "登陆成功"
            })
        else:
            return jsonify({
                "status": 2,
                "message": "登录失败"
            })

    return render_template('user_login.html')


# 注册
class RegisterForm(object):
    def validate_on_submit(self):
        pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = user(username=form.username.data,
                 password=form.password.data)
        db.session.add(u)
        db.session.commit()

        return jsonify({
            "status": 1,
            "message": "成功"
        })


# 退出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.html'))


# 用户资料
@app.route('/user/<username>')
def user(username):
    users = username.query.filter_by(username=username).first()
    if users is None:
        pass
    else:
        pass


# 发布活动
@app.route("/activity", method=['get'])
def Activity():
    pass


# 评论
@app.route('/comment', method=["get"])
def Comments():
    pass


if __name__ == '__main__':
    app.run(debug=True)
