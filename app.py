from itertools import product

from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from favorite import favorite
from product import product
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
    if request.method == 'POST':
        un = request.form.get('email')
        pw = request.form.get('password')
        if not un or not pw:
            return render_template('login.html', msg='Missing username or password')

        u = user()

        if u.tryLogin(un, pw):
            print(f'Login successful: {u.data[0]}')

            # session['user'] = u.data[0]['email']
            # session['active'] = time.time()
            # session['role'] = u.data[0]['role']

            session['user'] = {
                'id': u.data[0]['user_id'],
                'email': u.data[0]['email'],
                'role': u.data[0]['role'],
                'active': time.time()
            }

            return redirect('/home')
        else:
            print('Login failed')
            return render_template('login.html', msg='Invalid email or password')

    # GET request → just show page
    return render_template('login.html')  
def checksession():
    if 'user' in session and 'active' in session['user']:
        if time.time() - session['user']['active'] > 500:
            session['msg'] = 'Session has timed-out'
            return False
        else:
            session['user']['active'] = time.time()
            session['msg'] = 'Session is active'
            return True
    else:
        session['msg'] = 'Session is not active'
        return False
    
@app.route('/home')
def home_page():
    if checksession() == False:
        return redirect('/login')
    p = product()
    print('home loaded')
    print(session['user']['active'])

    items = p.getAll(session.get('user')['id'])
    return render_template('home.html', title='Home', msg=session.get('msg'), items=items, user=session.get('user')['email'], role=session.get('user')['role'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not first_name or not last_name or not email or not password:
            return render_template('signup.html', msg='All fields are required')

        u = user()

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'password2': password2,
            'role': 'participant'
        }

        u.set(data)

        if u.verifyNew():
            u.insert()
            return render_template('login.html', msg='Signup successful! Please login.')
        else:
            return render_template('signup.html', msg=u.errors, obj=u)

    return render_template('signup.html')

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    if session.get('user') is not None:
        del session['user']

    return render_template('login.html',title='Login', msg='you are on the login page')

@app.route("/users/manage",methods=['GET', 'POST'])
def manage_user():
    if checksession() == False:
        return redirect('/login')
    
    # pkval = request.args.get('pkval')
    # action = request.args.get('action')
    o = user()
    o.getAll()

    # if action == 'insert':
    #     d = {}
    #     d['name'] = request.form.get('name')
    #     d['email'] = request.form.get('email')
    #     d['role'] = request.form.get('role')
    #     d['password'] = request.form.get('password')
    #     d['password2'] = request.form.get('password2')

    #     o.set(d)
    #     if o.verify_new():
    #         o.insert()
    #         return render_template('ok_dialog.html', msg=f"user {o.data[0][o.pk]} is added")
    #     else:
    #         return render_template('users/add.html', obj=o)
    # if action == 'update':
    #     o.getById(pkval)
    #     o.data[0]['name'] = request.form.get('name')
    #     o.data[0]['email'] = request.form.get('email')
    #     o.data[0]['role'] = request.form.get('role')
    #     if request.form.get('password') is not None:
    #         o.data[0]['password'] = request.form.get('password')
    #         o.data[0]['password2'] = request.form.get('password2')                    
    #     if o.verify_update():
    #         o.update()
    #         return render_template('ok_dialog.html', msg=f"user {o.data[0][o.pk]} is updated")
    #     else:
    #         return render_template('users/manage.html', obj=o)
    # if action == 'delete':
    #     o.deleteById(pkval)
    #     return render_template('ok_dialog.html', msg=f"user is deleted")
    # if pkval is None:
    #     o.getAll()
    #     return render_template('users/list.html', obj=o)
    # if pkval == 'new':
    #     o.createBlank()
    #     return render_template('users/add.html', obj=o)
    # o.getById(pkval)
    return render_template('users/manage.html', obj=o)

@app.route('/products/manage/<int:product_id>',methods=['GET', 'POST'])
def manage_product(product_id):
    if checksession() == False:
        return redirect('/login')
    
    p = product()
    product_data = p.getbyProductId(product_id)
    # action = request.args.get('action')
    return render_template('products/manage.html', product=product_data, role=session.get('user')['role'])

@app.route('/product/<int:product_id>')
def view_product(product_id):
    p = product()
    product_data = p.getbyProductId(product_id)

    return render_template(
        'products/item.html',
        product=product_data,
        role=session.get('user')['role']
    )

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if checksession() == False:
        return redirect('/login')
    
    if request.method == 'POST':
        p = product()

        data = {
            'product_name': request.form.get('product_name'),
            'description': request.form.get('description'),
            'product_price': request.form.get('product_price'),
            'seller_id': session.get('user')['id'],
            'product_condition': request.form.get('condition'),
            'product_status': 'available'
        }

        p.CreateListing(data)

        return redirect('/home')

    return render_template('products/add.html', role=session.get('user')['role'])

@app.route('/favorites')
def view_favorites():
    if checksession() == False:
        return redirect('/login')

    f = favorite()
    favorites = f.get_favorites(session.get('user')['id'])

    return render_template('favorite.html', items=favorites, role=session.get('user')['role'])

@app.route('/favorites/<int:product_id>', methods=['POST'])
def toggle_favorite(product_id):
    if checksession() == False:
        return redirect('/login')

    f = favorite()
    f.toggle_favorite(session.get('user')['id'], product_id)

    return redirect('/home')

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True)