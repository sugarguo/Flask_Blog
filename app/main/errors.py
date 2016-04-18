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

import os

from flask import render_template
from . import main
from ..models import User, Article, Packet, Site




def site_get():
    meminfo = {}
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)
    site_info = {}
    site_dict = Site.query.filter_by().first()
    if site_dict is not None:
        temp_dict = site_dict.__dict__
        del temp_dict["_sa_instance_state"]
        site_info = temp_dict
    else:
        site_info['site_name'] = 'Sugarguo_Flask_Blog'
        #site_info['site_domain'] = 'http://www.sugarguo.com/'
        site_info['site_email'] = 'sugarguo@live.com'
        
    site_info['memuse'] = int(meminfo['MemTotal'][:-3]) - int(meminfo['MemFree'][:-3])
    site_info['pids'] = len(pids)
    return site_info

@main.app_errorhandler(404)
def page_not_found(e):
    site_info = site_get()
    return render_template('error/404.html', **locals()), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    site_info = site_get()
    return render_template('error/500.html', **locals()), 500