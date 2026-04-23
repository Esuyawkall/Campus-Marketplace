import yaml
from pathlib import Path
import pymysql
import datetime
from order import order
from user import user
from product import product
from image import image
from baseObject import baseObject
from app import app
from message import message

# up = user()
# u.data = []
# u.getByField('email','esuyawkal4@clarkson.edu')
# u.data[0]['name'] = 'newName'
# if u.verifyUpdate():
#     u.update()
#     print(f"ID {u.data[0][u.pk]} updated")
#     u = user()
#     u.getAll()
#     print(f"new name is {u.data[0]['name']}")
# else:
#     print(u.errors)
# print(up.hashPassword('122abc'))
# print(up.roleList())

# d = {'first_name':'esuyawkal','last_name':'bereda','email':'esuyawkal@admin','password':'123','password2':'123', 'role': 'admin', 'user_status': 'active'}
# up.set(d)
# if up.verifyNew():
#     up.insert()
# else:
#     print(up.errors)


# if up.tryLogin('esuyawkal3@clarkson.edu','1234'):
#     print("Successfull login")
# else:
#     print("Unsuccessfull login")
# print(up.data)



#u = user()
#u.deleteById(14)  

# u = user()
# u.getAll()
# print(u.data)
# o = order()
# print(o.get_order_summary_by_user_id(2))

u = user()
d = {'first_name':'esuyawkal','last_name':'bereda','email':'esuyawkal@admin','password':'123','password2':'123', 'role': 'admin', 'user_status': 'active'}
u.set(d)
if u.verifyNew():
    u.insert()
    print(f"User created with ID {u.data[0][u.pk]}")
else:
    print(u.errors)

p = product()
data = {'product_name': 'Play Station 4', 
        'description': 'Selling my sparingly used PlayStation 5 (Disc Edition). This console works perfectly and has been taken excellent care of. It has only been used for roughly 20-30 hours since I bought it new. No scratches, never dropped, and comes from a smoke-free, pet-free home.', 
        'product_price': 650, 
        'product_condition': 'Used',
        'product_status': 'active',
        'image_url': 'images/playstation.jpg'
        }
product_id = 1
p.updateProduct(product_id, data)

p.deleteById(11)




