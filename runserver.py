#coding=utf-8
'''
Created on 2016年04月15日

@FileName: manage.py

@Description: (描述) 

@Site:  http://www.sugarguo.com/

@author: 'Sugarguo'

@version V1.0.0
'''

import os
import sys
import json
sys.path.insert(0,'ext_lib')

from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == '__main__':
    app.run()
