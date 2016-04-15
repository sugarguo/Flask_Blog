#! usr/bin/python
#  -_-  coding:utf-8 -_-


from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors