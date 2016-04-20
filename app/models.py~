#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月15日

@version         v1.0.0 

@copyright       Sugarguo

File             models.py

'''


from . import db
from . import login_manager

from datetime import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique = True, index = True)

    #recordings = db.relationship('Recording', backref = 'user')
    
    @property
    def password(self):
        raise AttributeError(u'禁止获取密码！')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User % r>' % self.username



class Packet(db.Model):
    __tablename__ = "packets"
    id = db.Column(db.Integer, primary_key = True)
    packet_name = db.Column(db.String(255), index = True, unique = True)
    
    def __repr__(self):
        return '<User % r>' % self.packetname


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), index = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    tags = db.Column(db.Text)
    packet_id = db.Column(db.Integer, index = True, default = 0)
    show = db.Column(db.Integer, default = 1)


    def __repr__(self):
        return '<Article % r>' % self.title
    
    
class Site(db.Model):
    __tablename__ = 'Sites'
    id = db.Column(db.Integer, primary_key = True)
    site_name = db.Column(db.String(255), unique = True)
    site_domain = db.Column(db.String(255), unique = True)
    site_email = db.Column(db.String(255), unique = True)
    site_time = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    
    
    def __repr__(self):
        return '<Site % r>' % self.site_name   


    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))