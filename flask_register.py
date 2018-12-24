from flask import Flask, render_template,g,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import sqlite3
import json
from form import FormRegister
from modell import UserReister
import os
import pymysql

#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data_register.sqlite')
app.config['SECRET_KEY']='abcd0392'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data_register.sqlite')
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db

@app.route('/testheader', methods=['GET', 'POST'])
def testheader():
    print (request.headers['your'])
    a = request.headers['your']
    return a

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        ret = request.get_json(force=True)
        #print (ret['question1'])
        #print (request.headers['your'])
        q1 = int(ret['question1'])
        q2 = int(ret['question2'])
        q3 = int(ret['question3'])
        q4 = int(ret['question4'])
        q5 = int(ret['question5'])
        q6 = int(ret['question6'])
        q7 = int(ret['question7'])
        q8 = int(ret['question8'])
        q9 = int(ret['question9'])
        q10 = int(ret['question10'])
        q11 = int(ret['question11'])
        q12 = int(ret['question12'])
        r =q1+q7
        i =q2+q8
        a =q3+q9
        s =q4+q10
        e =q5+q11
        c =q6+q12
        result = [r,i,a,s,e,c]
        if max(result) == result[0]:
            return '實際型~適合從事的活動:使用機器、工具及物件。適合職業:木匠，貨車或大農場管理人'
        elif max(result) == result[1]:
            return '探究型~適合從事的活動:探索及理解事件和物件。適合職業:心理學家，微生物學家或化學家'
        elif max(result) == result[2]:
            return '藝術型~適合從事的活動:閱讀，音樂或藝術活動、寫作。適合職業:音樂家，室內設計師或編輯'
        elif max(result) == result[3]:
            return '社交型~適合從事的活動:幫助他人，教導，輔導或服務他人。適合職業:輔導員，神職人員或教職'
        elif max(result) == result[4]:
            return '企業型~適合從事的活動:遊說或指導他人。適合職業:律師，零售店經理或生產商'
        else :
            return '規律型~適合從事的活動:執行有秩序的例行公事，符合清楚的標準。適合職業:影視製作剪接員，速記員或文員'

        #return json.dumps(result.index(max(result)))
        #return json.dumps(result[0])

    return 'Not success'
@app.route('/DELETE/api/user/<id>', methods=['GET', 'POST'])
def delete(id):
    #from modell import UserReister
    from modell import db

    users=UserReister.query.filter_by(id=id).first()
    db.session.delete(users)
    db.session.commit()
    return 'Success Thank You'
@app.route('/GET/api/user', methods=['GET', 'POST'])
def user():
    class UserEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, UserReister):
                return obj.id,obj.username,obj.email,obj.password
            return json.JSONEncoder.default(self, obj)

    from modell import UserReister
    #db = get_db()
    #cursor = db.cursor()
    #cursor.execute("SELECT * FROM UserRegisters")
    users=UserReister.query.all()
    #ret = cursor.fetchall()

    print (users)
    print (type(json.dumps(users,cls=UserEncoder)))
    #print (json.dumps(users))
    #return jsonify(users)
    #return jsonify({'username':'wang123123'})
    #j2={'user':UserReister('username':'wang123123')}
    return json.dumps(users,cls=UserEncoder)
    #return 'thing'

@app.route('/register', methods=['GET', 'POST'])
def register():
    from form import FormRegister
    from modell import UserReister
    form =FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
            #username = '1111111111111111111',
            #email = '1111@11111111111111',
            #password = '111111111111111111'
        )
        db.session.add(user)
        db.session.commit()
        return 'Success Thank You'
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()