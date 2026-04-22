from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from favorite import favorite
from image import image
from order import order
from product import product
from user import user
from message import message
from flask import jsonify

import time

import os
from werkzeug.utils import secure_filename
from flask import request

app = Flask(__name__, static_url_path='')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

DEFAULT_IMAGE = 'images/desk+chair.jpg'

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['SECRET_KEY'] = 'sdfvbgfdjeR5y5r'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

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

            session['user'] = {
                'id': u.data[0]['user_id'],
                'email': u.data[0]['email'],
                'role': u.data[0]['role'],
                'first_name': u.data[0]['first_name'],
                'last_name': u.data[0].get('last_name', ''),
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
    msg = f'Login successful, User: {session.get("user")["first_name"]} ({session.get("user")["role"]})!'

    is_admin = session.get('user')['role'] == 'admin'
    
    # Get search query
    search = request.args.get('q', '')
    
    # Get all items (from other sellers) with search
    items = p.getAll(session.get('user')['id'], is_admin=is_admin, search=search)
    
    # Get my items with search
    myItems = p.getbySellerId(session.get('user')['id'], search=search)
    
    # Get user's ordered products
    o = order()
    user_orders = o.get_orders(session.get('user')['id'])
    ordered_product_ids = set(item['product_id'] for item in user_orders)

    for item in items:
        item['img_url'] = item.get('image_url') or DEFAULT_IMAGE
        item['already_ordered'] = item['product_id'] in ordered_product_ids
    for item in myItems:
        item['img_url'] = item.get('image_url') or DEFAULT_IMAGE
    return render_template('home.html', title='Home', msg=msg, items=items, myItems=myItems, user=session.get('user')['email'], role=session.get('user')['role'], search_query=search)

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

@app.route('/profile')
def profile_page():
    if not checksession():
        return redirect('/login')

    u = user()
    u.getById(session['user']['id'])
    profile_user = u.data[0] if u.data else session['user']

    # Keep session display fields in sync after profile data changes.
    session['user']['first_name'] = profile_user.get('first_name', session['user']['first_name'])
    session['user']['last_name'] = profile_user.get('last_name', session['user'].get('last_name', ''))
    session['user']['email'] = profile_user.get('email', session['user']['email'])
    session['user']['role'] = profile_user.get('role', session['user']['role'])

    return render_template(
        'users/profile.html',
        title='Profile',
        user=profile_user,
        role=session['user']['role']
    )

@app.route("/users/manage",methods=['GET', 'POST'])
def manage_user():
    if checksession() == False:
        return redirect('/login')
    
    if session.get('user')['role'] != 'admin':
        return redirect('/home')
    
    # Handle POST request for banning user
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        
        if user_id:
            try:
                # Delete all products by this user
                p = product()
                p_sql = f'''DELETE FROM `{p.tn}` WHERE `seller_id` = %s;'''
                p.cur.execute(p_sql, [user_id])
                
                # Delete the user
                u = user()
                u.deleteById(user_id)
                
                return redirect('/users/manage')
            except Exception as e:
                print(f"Error banning user: {e}")
                return redirect('/users/manage')
    
    # GET request - display all users
    u = user()
    u.getAll()
    
    return render_template('users/manage.html', items=u.data, role=session.get('user')['role'])

@app.route('/user/<int:user_id>')
def view_user_profile(user_id):
    if checksession() == False:
        return redirect('/login')
    
    # Get user info
    u = user()
    u.getById(user_id)
    
    if not u.data:
        return redirect('/home')
    
    profile_user = u.data[0]
    current_user = session.get('user')
    
    # Get user's listings
    p = product()
    sql = f'''SELECT * FROM `{p.tn}` WHERE `seller_id` = %s AND `product_status` = 'available';'''
    p.cur.execute(sql, [user_id])
    user_listings = p.cur.fetchall()
    
    # Set image URLs for listings
    for item in user_listings:
        item['img_url'] = item.get('image_url') or DEFAULT_IMAGE
    
    # Get user's messages
    m = message()
    user_messages = m.getMessagesByUserId(user_id)
    
    return render_template(
        'users/user_profile.html',
        user=profile_user,
        listings=user_listings,
        messages=user_messages,
        current_user_id=current_user['id'],
        current_role=current_user['role']
    )

@app.route('/product/<int:product_id>')
def view_product(product_id):
    if checksession() == False:
        return redirect('/login')
    p = product()
    product_data = p.getbyProductId(product_id)
    if not product_data:
        return redirect('/home')

    current_user = session.get('user')
    is_admin = current_user['role'] == 'admin'
    is_seller = product_data['seller_id'] == current_user['id']
    status = (product_data.get('product_status') or 'available').lower()

    if status == 'unavailable' and not (is_admin or is_seller):
        return redirect('/home')

    # Check if user has already ordered this product
    o = order()
    has_ordered = o.has_user_ordered_product(current_user['id'], product_id)
    
    can_order = (status == 'available') and not is_seller and not has_ordered
    if is_seller:
        block_reason = 'You cannot order your own listing.'
    elif has_ordered:
        block_reason = 'You have already purchased this item.'
    elif status == 'pending':
        block_reason = 'This listing is pending review and cannot be ordered yet.'
    elif status == 'unavailable':
        block_reason = 'This listing is unavailable right now.'
    else:
        block_reason = ''

    i = image()
    joined_url = product_data.get('image_url')

    if joined_url and isinstance(joined_url, str) and joined_url.strip() and (
        joined_url.startswith('http://') or joined_url.startswith('https://')
    ):
        product_data['image_url'] = joined_url
    else:
        product_data['image_url'] = product_data.get('image_url') or DEFAULT_IMAGE

    return render_template(
        'products/item.html',
        product=product_data,
        role=current_user['role'],
        can_order=can_order,
        block_reason=block_reason
    )

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if checksession() == False:
        return redirect('/login')
    
    if request.method == 'POST':
        p = product()

        file = request.files.get('image')  # 🔥 get file instead of form text
        image_path = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            import uuid
            unique_name = f"{uuid.uuid4().hex}_{filename}"

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)

            # store relative path ONLY
            image_path = f"images/{unique_name}"
        else:
            image_path = None  # or default image

        data = {
            'product_name': request.form.get('product_name'),
            'description': request.form.get('description'),
            'product_price': request.form.get('product_price'),
            'seller_id': session.get('user')['id'],
            'product_condition': request.form.get('condition'),
            'product_status': 'available',
            'image_url': image_path
        }

        p.CreateListing(data)
        print(f"Created product with data: {data}")

        return redirect('/home')

    return render_template('products/add.html', role=session.get('user')['role'])
@app.route('/products/manage/<int:product_id>', methods=['GET', 'POST'])
def manage_product(product_id):
    if not checksession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect(url_for('edit_product', product_id=product_id))

    p = product()
    product_data = p.getbyProductId(product_id)

    if request.method == 'GET':
        return render_template(
            'products/manage.html',
            product=product_data,
            role=session['user']['role']
        )

    # 🔵 UPDATE DATA (POST)
    if request.method == 'POST':
        # Check if delete button was clicked
        if request.form.get('action') == 'delete':
            p.deleteProduct(product_id)
            return redirect('/home')
        
        # Otherwise, it's an update
        data = {
            'product_name': request.form.get('product_name'),
            'description': request.form.get('description'),
            'product_price': request.form.get('product_price'),
            'product_condition': request.form.get('condition'),
            'product_status': request.form.get('product_status') or 'available',
        }

        file = request.files.get('image')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            import uuid
            unique_name = f"{uuid.uuid4().hex}_{filename}"

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)

            data['image_url'] = f"images/{unique_name}"
        else:
            data['image_url'] = product_data['image_url']

        p.updateProduct(product_id, data)

        return redirect('/home')

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not checksession():
        return redirect('/login')

    p = product()
    product_data = p.getbyProductId(product_id)
    if not product_data:
        return redirect('/home')

    is_admin = session['user']['role'] == 'admin'
    is_seller = product_data['seller_id'] == session['user']['id']
    if not (is_admin or is_seller):
        return redirect('/home')

    if request.method == 'POST':
        # Check if delete button was clicked
        if request.form.get('action') == 'delete':
            p.deleteProduct(product_id)
            return redirect('/home')
        
        # Otherwise, it's an update
        data = {
            'product_name': request.form.get('product_name'),
            'description': request.form.get('description'),
            'product_price': request.form.get('product_price'),
            'product_condition': request.form.get('condition'),
            'product_status': product_data['product_status']  # Keep existing status
        }
        
        file = request.files.get('image')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            import uuid
            unique_name = f"{uuid.uuid4().hex}_{filename}"

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)

            image_path = f"images/{unique_name}"
        else:
            image_path = product_data['image_url']

        data['image_url'] = image_path
        p.updateProduct(product_id, data)
        return redirect('/home')

    return render_template(
        'products/edit.html',
        product=product_data,
        role=session['user']['role']
    )

@app.route('/favorites', methods=['GET', 'POST'])
def view_favorites():
    if checksession() == False:
        return redirect('/login')

    f = favorite()
    favorites = f.get_favorites(session.get('user')['id'])

    for item in favorites:
        item['img_url'] = item.get('image_url') or DEFAULT_IMAGE

    return render_template('favorite.html', items=favorites, role=session.get('user')['role'])

@app.route('/favorites/<int:product_id>', methods=['GET', 'POST'])
def toggle_favorite(product_id):
    if checksession() == False:
        return redirect('/login')

    f = favorite()
    liked = f.toggle_favorite(session.get('user')['id'], product_id)

    return  jsonify({"liked": liked})


def build_orders_page_data(user_id):
    o = order()
    orders = o.get_orders(user_id)
    i = image()

    for item in orders:
        item['img_url'] = item.get('image_url') or DEFAULT_IMAGE

    stats = o.get_user_order_stats(user_id) or {}
    order_stats = {
        'buyer_total_orders': stats.get('buyer_total_orders', 0),
        'buyer_completed_orders': stats.get('buyer_completed_orders', 0),
        'buyer_pending_orders': stats.get('buyer_pending_orders', 0),
        'buyer_other_orders': stats.get('buyer_other_orders', 0),
        'buyer_total_spend': stats.get('buyer_total_spend', 0),
        'buyer_completed_spend': stats.get('buyer_completed_spend', 0),
        'buyer_pending_spend': stats.get('buyer_pending_spend', 0),
        'seller_total_sales': stats.get('seller_total_sales', 0),
        'seller_completed_sales': stats.get('seller_completed_sales', 0),
        'seller_pending_sales': stats.get('seller_pending_sales', 0),
        'seller_other_sales': stats.get('seller_other_sales', 0),
        'seller_total_sales_value': stats.get('seller_total_sales_value', 0),
        'seller_completed_revenue': stats.get('seller_completed_revenue', 0),
        'seller_pending_revenue': stats.get('seller_pending_revenue', 0),
        'seller_avg_sale_value': stats.get('seller_avg_sale_value', 0),
        'seller_largest_sale': stats.get('seller_largest_sale', 0)
    }
    return orders, order_stats

@app.route('/orders', methods=['GET', 'POST'])
def view_orders():
    if checksession() == False:
        return redirect('/login')
    print('home loaded')
    print(session['user']['active'])

    orders, order_stats = build_orders_page_data(session.get('user')['id'])
    return render_template('order.html', orders=orders, order_stats=order_stats, role=session.get('user')['role'])
@app.route('/orders/<int:product_id>', methods=['GET', 'POST'])
def place_order(product_id):
    if checksession() == False:
        return redirect('/login')
    p = product()
    product_data = p.getbyProductId(product_id)
    status = (product_data.get('product_status') if product_data else 'unavailable')
    current_user = session.get('user')
    is_admin = current_user['role'] == 'admin'
    is_seller = product_data and product_data['seller_id'] == current_user['id']

    if (not product_data) or (status != 'available') or is_seller:
        orders, order_stats = build_orders_page_data(current_user['id'])

        if is_seller:
            msg = 'You cannot order your own listing.'
        elif status == 'pending':
            msg = 'This listing is pending review and cannot be ordered yet.'
        elif status == 'unavailable':
            msg = 'This listing is unavailable and cannot be ordered.'
        else:
            msg = 'This listing cannot be ordered.'

        # Prevent users from ordering hidden unavailable listings.
        if status == 'unavailable' and not is_admin and not is_seller:
            return redirect('/home')

        return render_template('order.html', msg=msg, orders=orders, order_stats=order_stats, role=current_user['role'])

    o = order()
    result = o.place_order(current_user['id'], product_id, quantity=1)
    orders, order_stats = build_orders_page_data(current_user['id'])

    if 'error' in result:
        return render_template('order.html', msg=result['error'], orders=orders, order_stats=order_stats, role=session.get('user')['role'])
    else:        
        return render_template('order.html', msg=result['success'], orders=orders, order_stats=order_stats, role=session.get('user')['role'])
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if not checksession():
        return redirect('/login')

    m = message()
    inbox = m.getMessagesByUserId(session['user']['id'])

    return render_template(
        'message.html',
        messages=inbox,
        role=session['user']['role']
    )
@app.route('/chat/<int:user_id>')
def chat(user_id):
    if not checksession():
        return redirect('/login')

    m = message()
    product_id = request.args.get('product_id', type=int)
    
    chat_messages = m.getMessagesBetweenUsers(
        session['user']['id'],
        user_id,
        product_id=product_id
    )

    return render_template(
        'messages/chat.html',
        messages=chat_messages,
        receiver_id=user_id,
        current_user=session['user']['id'],
        role=session['user']['role'],
        product_id=product_id
    )
@app.route('/chat/send/<int:receiver_id>', methods=['POST'])
def send_message(receiver_id):
    if not checksession():
        return {"error": "unauthorized"}, 401

    data = request.get_json()
    product_id = data.get('product_id')

    m = message()
    m.sendMessage(
        session['user']['id'],
        receiver_id,
        data['message'],
        product_id=product_id
    )

    return {"status": "ok"}

@app.route('/admin/messages')
def admin_messages():
    if not checksession():
        return redirect('/login')
    
    if session['user']['role'] != 'admin':
        return redirect('/home')
    
    m = message()
    all_messages = m.getAllMessages()

    return render_template(
        'messages/admin_messages.html',
        messages=all_messages,
        role=session['user']['role']
    )

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True)
