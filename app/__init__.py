#! usr/bin/python
#  -_-  coding:utf-8 -_-


from flask import Flask, render_template, flash, redirect, url_for, request
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'
login_manager.login_message = u"欢迎登陆，您可以创建/修改/删除 文章！"



def create_app(config_name):
    app = Flask(__name__, static_url_path='/app/static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    
    db.init_app(app)
    login_manager.init_app(app)
    
    return app
