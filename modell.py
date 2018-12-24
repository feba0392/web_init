from flask import Flask
#  from flask.ext.sqlalchemy import SQLAlchemy<--新版取消了
from flask_sqlalchemy import SQLAlchemy
import os

#  取得目前文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置sqlite檔案路徑
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(pjdir, 'data_register.sqlite')

db = SQLAlchemy(app)
class UserReister(db.Model):
    """記錄使用者資料的資料表"""
    __tablename__ = 'UserRegisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)