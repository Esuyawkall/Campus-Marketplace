
from pathlib import Path
import pymysql
import datetime
import hashlib
from baseObject import baseObject

class user(baseObject):
    def __init__(self):
        self.setup()
        print(type(self).__name__)
        self.roles = [{'value': 'admin', 
                       'text': 'Admin'},
                       {'value': 'participant',
                       'text': 'Participant'}]

    def verifyNew(self):
        self.errors = []
        if '@' not in self.data[0]['email']:
            self.errors.append('Email must contain @')
        if self.data[0]['role'] not in self.roleList():
            self.errors.append('Role does not exist')
        if len(self.data[0]['password']) < 3:
            self.errors.append('Password is too short')
        if self.data[0]['password2'] !=  self.data[0]['password']:
            self.errors.append('The two password do no match')
        self.data[0]['password'] = self.hashPassword(self.data[0]['password'])
        u = user()
        u.getByField('email',self.data[0]['email'])
        if len(u.data) > 0:
            self.errors.append(f"Email address is already in use. ({self.data[0]['email']})")
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    def tryLogin(self,un, pw):
        self.data = []
        pw = self.hashPassword(pw)
        sql = f'''SELECT * FROM `{self.tn}` WHERE `email` = %s AND `password` = %s;'''
        self.cur.execute(sql,[un,pw])
        for row in self.cur:
            self.data.append(row)
        if len(self.data) == 1:
            return True
        return False
    def roleList(self):
        roleLists = []
        for item in self.roles:
            roleLists.append(item['value'])
        return roleLists
    def hashPassword(self, password):
        password += 'xyz'
        return hashlib.md5(password.encode('utf-8')).hexdigest()
    def update(self):
        tokens = []
        sql = f'''UPDATE {self.tn} SET '''
        for field in self.fields:
            sql+= f'{field} = %s, '
            tokens.append(self.data[0][field])
        sql = sql[:-2]
        sql+= f' WHERE {self.pk} = %s'
        tokens.append(self.data[0][self.pk])
        self.cur.execute(sql,tokens)
    
    def verifyUpdate(self):
        self.errors = []
        if '@' not in self.data[0]['email']:
            self.errors.append('Email must contain @')
        if self.data[0]['role'] not in self.roleList():
            self.errors.append('Role does not exist')
        if len(self.data[0]['password']) < 3:
            self.errors.append('Password is too short')
        self.data[0]['password'] = self.hashPassword(self.data[0]['password'])
        u = user()
        u.getByField('email',self.data[0]['email'])
        if len(u.data) > 0 and u.data[0][self.pk] != self.data[0][self.pk]:
            self.errors.append(f"Email address is already in use. ({self.data[0]['email']})")
        
        if len(self.errors) == 0:
            return True
        else:
            return False
u = user()
