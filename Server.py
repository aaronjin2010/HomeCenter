import flask
import json
import os.path
import datetime

app = flask.Flask(__name__)

msg = list()

@app.route('/')
def main():
    data = list()
    username = str()
    if 'user' in flask.request.cookies.keys():
        username = flask.request.cookies['user']
    else:
        username = ''
    with open('data.json', mode='r') as f:
        data = json.loads((f.read()))
        data.reverse()
        return flask.render_template("home.html", data=data, user=username)

@app.route('/pub', methods=['GET', 'POST'])
def publish():
    if flask.request.method == 'POST':
        userdata = dict(flask.request.form)
        userdata['time'] = datetime.datetime.now().strftime('%Y年 %m月 %d日 %H:%M')
        userdata['name'] = flask.request.cookies['user']
        with open('data.json', mode='r') as f:
            msg = json.loads((f.read()))           
        msg.append(userdata)
        # print(msg)
        with open('data.json', mode='w') as f:
            f.write(json.dumps(msg))
        return flask.render_template('ok.html', title='提交成功！', msg='提交成功！', link='/')
    else:
        if 'user' in flask.request.cookies.keys():
            return flask.render_template('publish.html')
        else:
            return flask.render_template('ok.html', title='请先登录', msg='请先登录！', link='/login')
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        userdata = dict(flask.request.form)
        with open('user.json', mode='r') as f:
            db = json.loads((f.read()))           
        username = userdata['name']
        password = userdata['pswd']
        if not (username in db.keys()):
            return flask.render_template('ok.html', title='用户不存在！', msg='该用户不存在！', link='/login')
        elif db[username] != password:
            return flask.render_template('ok.html', title='密码错误！', msg='密码错误！', link='/login')
        else:
            resp = flask.make_response(flask.render_template('ok.html', title='登录成功！', msg='登录成功！', link='/'))
            resp.set_cookie('user', username)
            return resp
    else:
        if 'user' in flask.request.cookies.keys():
            return flask.render_template('ok.html', title='您已登录', msg='您已登录，请勿重复登录！', link='/')
        else:
            return flask.render_template('login.html')

@app.route('/logout')
def logout():
    resp = flask.make_response(flask.render_template('ok.html', title='登出', msg='您已登出！', link='/'))
    resp.delete_cookie('user')
    return resp

@app.route('/reg', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        userdata = dict(flask.request.form)
        with open('user.json', mode='r') as f:
            db = json.loads((f.read()))           
        username = userdata['name']
        password = userdata['pswd']
        if username == '':
            return flask.render_template('ok.html', title='用户名不能为空', msg='用户名不能为空！', link='/reg')
        elif username in db.keys():
            return flask.render_template('ok.html', title='该用户已存在', msg='该用户已存在！', link='/reg')
        else:
            resp = flask.make_response(flask.render_template('ok.html', title='注册成功！', msg='注册成功！', link='/'))
            resp.set_cookie('user', username)
            db[username] = password
            with open('user.json', mode='w') as f:
                f.write(json.dumps(db))
            return resp
    else:
        return flask.render_template('register.html')

if __name__ == '__main__':
    if not os.path.exists('data.json'):
        f = open('data.json', 'w')
        f.write('[]')
        f.close()
    if not os.path.exists('user.json'):
        f = open('user.json', 'w')
        f.write('{}')
        f.close()
    app.run(host='0.0.0.0', port=8080, debug=True)