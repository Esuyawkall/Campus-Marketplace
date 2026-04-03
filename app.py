from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from user import user

import time
import datetime

app = Flask(__name__,static_url_path='')

app.config['SECRET_KEY'] = 'sdfvbgfdjeR5y5r'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login' , methods=['GET','POST'])
def login():
    un = request.form.get('email')
    pw = request.form.get('password')

    if un is not None and pw is not None:
        u = user()
        if u.tryLogin(un, pw):
            print(f'Login successful: {u.data[0]}')
            session['user'] =u.data[0]
            session['active'] = time.time()
            return redirect('/home')
        else:
            print('Login failed')
            return render_template('login.html', msg='Login failed')  
    else:
        return render_template('login.html', msg='Missing username or password')
def checksession():
    if 'active' in session.keys():
        if time.time() - session['active'] > 500:
            session['msg'] = 'Session has timed-out'
            return False
        else:
            session['active'] = time.time()
            session['msg'] = 'Session is active'
            return True
    else:
        session['msg'] = 'Session is not active'
        return False
    
@app.route('/home')
def home_page():
    if checksession() == False:
        return redirect('/login')
    print('home loaded')
    print(session['active'])
    return render_template('home.html',title='Home', msg=session['msg'], user=session['user'])

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    if session.get('user') is not None:
        # print(f'This is you {session}')
        del session['active']
        del session['user']
        del session['msg']
    return render_template('login.html',title='Login', msg='you are on the login page')

@app.route("/users/manage",methods=['GET', 'POST'])
def manage_user():
    if checksession() == False:
        return redirect('/login')
    pkval = request.args.get('pkval')
    action = request.args.get('action')
    o = user()
    if action == 'insert':
        d = {}
        d['name'] = request.form.get('name')
        d['email'] = request.form.get('email')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')

        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html', msg=f"user {o.data[0][o.pk]} is added")
        else:
            return render_template('users/add.html', obj=o)
    if action == 'update':
        o.getById(pkval)
        o.data[0]['name'] = request.form.get('name')
        o.data[0]['email'] = request.form.get('email')
        o.data[0]['role'] = request.form.get('role')
        if request.form.get('password') is not None:
            o.data[0]['password'] = request.form.get('password')
            o.data[0]['password2'] = request.form.get('password2')                    
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html', msg=f"user {o.data[0][o.pk]} is updated")
        else:
            return render_template('users/manage.html', obj=o)
    if action == 'delete':
        o.deleteById(pkval)
        return render_template('ok_dialog.html', msg=f"user is deleted")
    if pkval is None:
        o.getAll()
        return render_template('users/list.html', obj=o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html', obj=o)
    else:
        o.getById(pkval)
        return render_template('users/manage.html', obj=o)
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True)