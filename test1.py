import yaml
from pathlib import Path
import pymysql
import datetime
from user import user

up = user()
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

d = {'first_name':'esuyawkal','last_name':'bereda','email':'esuyawkal@admin','password':'123','password2':'123', 'role': 'admin', 'user_status': 'active'}
up.set(d)
if up.verifyNew():
    up.insert()
else:
    print(up.errors)


# if up.tryLogin('esuyawkal3@clarkson.edu','1234'):
#     print("Successfull login")
# else:
#     print("Unsuccessfull login")
# print(up.data)



#u = user()
#u.deleteById(14)  