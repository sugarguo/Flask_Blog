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


import json
import time

from datetime import datetime, date
from flask import render_template, session, redirect, url_for, request, make_response, flash
from flask.ext.login import login_required, current_user

from . import main
from .. import db
from ..models import User, Article, Packet



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
    titlename = u"Sugarguo_Flask_Blog"
    article_id = request.args.get('article_id',0)
    body = u"巴拉巴拉"
    tempdict = {}
    packet_dict = {}
    article_dict = []
    packet_list = Packet.query.filter_by().all()
    if packet_list is not None:
        for temp in packet_list:
            tempdict = temp.__dict__
            del tempdict["_sa_instance_state"]
            packet_dict = dict( packet_dict.items() + tempdict.items() )
            
    tempdict = {}
    article_list = Article.query.filter_by(show = 1).all()
    if article_list is not None:
        for temp in article_list:
            tempdict = temp.__dict__
            article_dict.append([tempdict["id"],tempdict["title"],tempdict["timestamp"].strftime('%Y-%m-%d')])
            
    print article_dict
    print article_dict[0][0]

    return render_template('index.html', **locals())
    
    
@main.route('/about')
def about():
    titlename = u"Sugarguo_Flask_Blog"

    return render_template('about.html', **locals())



@main.route('/article')
def article():
    titlename = u"Sugarguo_Flask_Blog"
    article_id = request.args.get('article_id',0)

    if article_id != 0:
        article = Article.query.filter_by(id = article_id).first()
        print article
        if article is not None:
            article = article.__dict__
            title = article['title']
            packet_id = article['packet_id']
            show = article['show']
            timestamp = article['timestamp']
            body = article['body'][:-1]
            print 'do'
    else:
        return redirect(url_for('main.index'))

    return render_template('article.html', **locals())