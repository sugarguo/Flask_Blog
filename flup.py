#! usr/bin/python
#  -_-  coding:utf-8 -_-

import os
import sys
import json
sys.path.insert(0,'ext_lib')
from flup.server.fcgi import WSGIServer
from app import create_app#, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    #app.run(debug=True,host='127.0.0.1',port=8889)

	WSGIServer(app, bindAddress=('127.0.0.1',8889)).run()
    #WSGIServer(app, bindAddress='/tmp/weeklyreport-fcgi.sock').run()

