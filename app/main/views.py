#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月15日

@version         v1.0.0 

@copyright       Sugarguo

File             main/views.py

'''


import os
import json
import time

from datetime import datetime, date
from flask import render_template, session, redirect, url_for, request, make_response, flash
from flask.ext.login import login_required, current_user

from . import main
from .. import db
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

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


@main.route('/')
def index():
    site_info = site_get()
    article_id = request.args.get('article_id',0)
    body = u"巴拉巴拉"
    article_dict = []
    temp_dict = {}
    packet_dict = {}
    packet_list = Packet.query.filter_by().all()
    if packet_list is not None:
        for temp in packet_list:
            temp_dict = temp.__dict__
            del temp_dict["_sa_instance_state"]
            packet_dict[str(temp_dict['id'])] = temp_dict['packet_name']
            
    tempdict = {}
    article_list = Article.query.filter_by(show = 1).all()
    if article_list is not None:
        for temp in article_list:
            tempdict = temp.__dict__
            article_dict.append([tempdict["id"],tempdict["title"],tempdict["timestamp"].strftime('%Y-%m-%d'),tempdict["body"][:150]])

    return render_template('index.html', **locals())
    
    
@main.route('/about')
def about():
    site_info = site_get()

    return render_template('about.html', **locals())



@main.route('/article')
def article():
    site_info = site_get()
    article_id = request.args.get('article_id',0)

    if article_id != 0:
        article = Article.query.filter_by(id = article_id).first()
        if article is not None:
            article = article.__dict__
            article_id = article['id']
            title = article['title']
            packet_id = article['packet_id']
            show = article['show']
            timestamp = article['timestamp']
            body = article['body'][:-1]
    else:
        return redirect(url_for('main.index'))

    return render_template('article.html', **locals())
