import sys
from io import BytesIO
from flask import Flask, jsonify
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask import request,redirect
from flask import url_for,flash

import pymysql
import json
import logging
import http.client    #修改引用的模块
import urllib
import urllib.request


app = Flask(__name__)
bootstrap = Bootstrap(app)
CORS(app, resources=r'/*')

@app.route('/book', methods=['GET'])
def getLoginRequest():
	#查詢使用者名稱及密碼是否匹配及存在
	#連線資料庫,此前在資料庫中建立資料庫TESTDB
	db = pymysql.connect(host = "140.118.110.32",port=53306,user = "ws_user",passwd = "ws_fall108",db = "ilibrary_test" )
	# 使用cursor()方法獲取操作遊標 
	cursor = db.cursor()
	# SQL 查詢語句
	sql = "select * from book "
	cursor.execute("show columns from book")
	ret = cursor.fetchall()
	#print(ret)
	try:
		thing = []
		# 執行sql語句
		cursor.execute(sql)
		results = cursor.fetchall()
		print(len(results))
		for d in results:
			print(d)
			thing.append(d)
		#app.logger.error('testing warning log')
		#_json = [{ name : 'hamimi', age : 3}]
		#print (_json)
		return jsonify(thing)
		#return 'connet db'
		
	except:
		# 如果發生錯誤則回滾
		return '不正確'
		traceback.print_exc()
	db.rollback()
	# 關閉資料庫連線
	db.close()
def login_check(username, password):
    """登入帳號密碼檢核"""
    if username == '1' and password == '2':
        return True
    else:
        return False
		
@app.route('/first', methods=['GET', 'POST'])
def first():		
    if request.method == 'POST':
		#return render_template('code.html',code =request.args.get('code') )
        return redirect("http://140.118.110.32:50080/oauth/web/login?response_type=code&client_id=m10709310&state=programming_homework_2&redirect_uri=http://127.0.0.1:5000/getcode")
    return render_template('first.html')
@app.route('/getcode', methods=['GET', 'POST'])
def getcode():
	if request.method == 'POST':
		#return render_template('code.html',code =request.args.get('code') )
		return render_template('code.html',code ='55564564564' )
	return render_template('code.html', code =request.args.get('code'))
 
@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    print(request.values['username'])
    params = urllib.parse.urlencode({'grant_type': 'authorization_code', 'client_id': 'm10709310', 'client_secret': 'cad104e02eb471a41be02aa5eadb0eb2d27593fd', 'code':request.values['username'], 'redirect_uri': 'http://127.0.0.1:5000/getcode'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
 
    httpClient = http.client.HTTPConnection("140.118.110.32", 50080, timeout=30)
    httpClient.request("POST", "/oauth/web/token", params, headers)
 
    response = httpClient.getresponse()
    #print (response.read())
    result = json.loads(response.read())
    print (result)
    #print (response.status)
    #print (response.reason)
    #print (response.read())
    #print (response.getheaders()) #获取头信息
    return render_template('authorize.html',res_a = result["access_token"],res_r = result["refresh_token"])
	
@app.route('/resource', methods=['GET', 'POST'])
def resource():
    # 查詢參數
    #my_params = {'access_token':request.values['username']}

# 將查詢參數加入 GET 請求中
    #r = requests.get('http://http://140.118.110.32:50080/oauth/web/resource', params = my_params)
    #print(r.text)
    print(request.values['username'])
    #params = urllib.parse.urlencode({'access_token':request.values['username']})
    #headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
 
   
 
    #httpClient = http.client.HTTPConnection('140.118.110.32', 50080, timeout=30)
    #print(request.values['username'])
    #token = request.values['username']
    #print(token)
    uri = "/oauth/web/resource?access_token=" + request.values['username']
    #print(uri)
    #print(str(uri))
    #httpClient.request('GET',uri)
    #httpClient.request('GET','/oauth/web/resource?access_token='+request.values['username'])
    r = urllib.request.urlopen('http://140.118.110.32:50080/oauth/web/resource?access_token='+request.values['username'])
    #print(r.read())	
    #httpClient.request('GET', '/oauth/web/resource?access_token=c6733eeb0d1aeabf294e4e9eb6d211fad479db60')
    
    #response = httpClient.getresponse()
    #print (response.status)
    #print (response.reason)
    #print(response.read())
    a=json.loads(r.read())
    print (a)
    #result = {"first_name":"Sheng"}
    #result = json.loads(response.read())
    #result = json.loads(r.read())
    #print (json.loads(r.read()))
    #print (12121212121212)
    #print (response.read())
    #print (12121212121212)
    #print (response.getheaders()) #获取头信息
    #return render_template('resource.html',res = result["first_name"])
    return render_template('resource.html',res = a["first_name"])
	#return redirect("http://140.118.110.32:50080/oauth/web/resource?access_token="+request.values['username'])
@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    print(request.values['refresh'])
    params = urllib.parse.urlencode({'grant_type': 'refresh_token', 'client_id': 'm10709310', 'client_secret': 'cad104e02eb471a41be02aa5eadb0eb2d27593fd', 'refresh_token':request.values['refresh']})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
 
    httpClient = http.client.HTTPConnection("140.118.110.32", 50080, timeout=30)
    httpClient.request("POST", "/oauth/web/token", params, headers)
 
    response = httpClient.getresponse()
    #print (response.read())
    result = json.loads(response.read())
    print (result)
    #print (response.status)
    #print (response.reason)
    #print (response.read())
    #print (response.getheaders()) #获取头信息
    return render_template('authorize.html',res_a = result["access_token"],res_r = result["refresh_token"])
    #return render_template('refresh.html',res = a["first_name"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    #  利用request取得使用者端傳來的方法為何
    if request.method == 'POST':
        if login_check(request.form.get('username'), request.form['password']):
            flash('Login Success!')
                          #  利用request取得表單欄位值
            return redirect(url_for('hello',username = request.form.get('username')))
			#return 'Hello ' + request.form.get('username')
    
    #  非POST的時候就會回傳一個空白的模板
    return render_template('login.html')	
@app.route('/hello/<username>')
def hello(username):
	return render_template('hello.html',username = username)
    #return render_template('web.html')
	#return redirect(url_for('user'))
@app.route('/')
def index():
	return render_template('test.html')
    #return render_template('web.html')
	#return redirect(url_for('user'))

@app.route('/draw', methods=['POST'])
def test():
    group_name = request.form.get('group_name', 'ALL')
    return '<p>{}</p>'.format(group_name)
    #return redirect(url_for('user'))
    #return render_template('test.html')

@app.route('/user', methods=['GET'])
def user():
    return "<p>Hello !</p>"

	
@app.route('/u/<name>')
def ser(name):

    return "<p>Hello {}!</p>".format(name)

@app.route('/book/<id>')
def bookid(id):
	#查詢使用者名稱及密碼是否匹配及存在
	#連線資料庫,此前在資料庫中建立資料庫TESTDB
	db = pymysql.connect(host = "140.118.110.32",port=53306,user = "ws_user",passwd = "ws_fall108",db = "ilibrary_test" )
	# 使用cursor()方法獲取操作遊標 
	cursor = db.cursor()
	# SQL 查詢語句
	#sql = "select * from book where id =  '" + str(id) + "' "
	sql = "select * from book where id = {} ".format(id)
	try:
		thing = []
		# 執行sql語句
		cursor.execute(sql)
		results = cursor.fetchall()
		
		for d in results:
			print(d)
			thing.append(d)
		
		return jsonify(thing)
		
		
	except:
		# 如果發生錯誤則回滾
		return '不正確'
		traceback.print_exc()
	db.rollback()
	# 關閉資料庫連線
	db.close()	
app.secret_key = 'super secret key'
if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    
    app.run()