#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月15日

@version         v1.0.0 

@copyright       Sugarguo

File             main/errors.py

'''


from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    titlename = u"Sugarguo_Flask_Blog"
    return render_template('error/404.html', **locals()), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    titlename = u"Sugarguo_Flask_Blog"
    return render_template('error/500.html', **locals()), 500