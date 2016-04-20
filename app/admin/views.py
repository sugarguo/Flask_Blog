#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月15日

@version         v1.0.0 

@copyright       Sugarguo

File             admin/views.py

'''

import os
import time
import json
import random
from datetime import datetime, date

from flask import render_template, redirect, url_for, flash, request, make_response
from flask.ext.login import login_user, login_required, logout_user, current_user

from . import admin
from .. import db
from ..models import User, Article, Packet, Site
from manage import app


show_list = {
               "0" : u"不显示",
               "1" : u"显示"
               }

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


@admin.route('/login', methods = ['GET', 'POST'])
def login():
    site_info = site_get()
    if request.method == 'POST':
        username=request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password = request.form.get('password')):
            login_user(user, request.form.get('remember_me'))
            return redirect(url_for('admin.index'))
        flash(u'用户名或密码错误，请重试！')
    return render_template('admin/login.html', **locals())

@admin.route('/logout')
@login_required
def logout():
    site_info = site_get()
    logout_user()
    flash(u'你已经退出系统！')
    return redirect(url_for('main.index'))


def getinfo_TeamName(team_id):
    tempdict = {}
    tempname = ""
    teamteamlist = Team.query.filter_by(id = team_id).first()
    if teamteamlist is not None:
        tempdict = teamteamlist.__dict__
        return tempdict['name']
    
        
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


@admin.route('/index')
@login_required
def index():
    site_info = site_get()
    return render_template('admin/index.html', **locals())
    
    
@admin.route('/getarticle')
@login_required
def getarticle():
    tempdict = {}
    tempjson = "["
    articlelist = Article.query.filter_by().all()
    if articlelist is not None:
        for item in articlelist:
            tempdict = item.__dict__
            del tempdict["_sa_instance_state"]
            value = json.dumps(tempdict,cls=CJsonEncoder)
            tempjson += value + ","
        tempjson = tempjson[:-1] + "]"
    else:
        tempjson = ""
    return tempjson
    
    
@admin.route('/article')
@login_required
def article():
    site_info = site_get()
    
    global show_list
    show_dict = show_list
    packet_dict = {}
    packet_list = Packet.query.filter_by().all()
    if packet_list is not None:
        for temp in packet_list:
            temp_dict = temp.__dict__
            del temp_dict["_sa_instance_state"]
            packet_dict[str(temp_dict['id'])] = temp_dict['packet_name']
    
    return render_template('admin/article.html', **locals())
    

@admin.route('/postarticle', methods = ['GET', 'POST'])
@login_required
def psot_article():
    article_id = request.args.get('article_id',0)
    if request.method == 'POST':
        if article_id == 0:
            article = Article(
                title = request.form.get('title'),
                packet_id = request.form.get('packet_id'),
                show = request.form.get('show'),
                body = request.form.get('body'),
                timestamp = datetime.now()
            )
            db.session.add(article)
            db.session.commit()
            flash(u'文章发布完毕')
        else:
            article = Article.query.filter_by(id = article_id).first()
            if article is not None:
                article.title = request.form.get('title')
                article.packet_id = request.form.get('packet_id')
                article.show = request.form.get('show')
                article.body = request.form.get('body')
                article.timestamp = datetime.now()
                db.session.add(article)
                db.session.commit()
            flash(u'文章更新完毕')
            
    return redirect(url_for('admin.article'))


@admin.route('/postsite', methods = ['GET', 'POST'])
@login_required
def psot_site():
    article_id = request.args.get('article_id',0)
    if request.method == 'POST':
        site_info = Site.query.filter_by().first()
        if article is not None:
            site_info['site_name'] = request.form.get('site_name'),
            site_info['site_domain'] = request.form.get('site_domain'),
            site_info['site_email'] = request.form.get('site_email'),
            db.session.add(article)
            db.session.commit()
        flash(u'站点信息更新完毕')
            
    return redirect(url_for('admin.index'))



@admin.route('/delete', methods = ['GET', 'POST'])
@login_required
def delete_artpk():
    op = request.form.get('op')
    if request.method == 'POST':
        if op == 'dl_art':
            temp_infolist = request.form.get('temp_info')[:-1]
            temp_infolist = temp_infolist.split(",")
            for item in temp_infolist:
                article = Article.query.filter_by(id = item).first()
                if article is not None:
                    db.session.delete(article)
                    db.session.commit()
                else:
                    flash(u'出现错误')
                    break;
        elif op == 'd_pk':
            packet_id = request.form.get('packet_id')
            packet = Packet.query.filter_by(id = packet_id).first()
            if packet is not None:
                db.session.delete(packet)
                db.session.commit()
                flash(u'文章分组更新完毕')
            else:
                flash(u'出现错误')
        elif op == 'd_art':
            article_id = request.form.get('id')
            article = Article.query.filter_by(id = article_id).first()
            if article is not None:
                db.session.delete(article)
                db.session.commit()
            flash(u'文章删除完毕')
    return redirect(url_for('admin.article'))
    

@admin.route('/add', methods = ['GET', 'POST'])
@login_required
def add_artpk():
    op = request.form.get('op')
    if request.method == 'POST':
        if op == 'ul_art':
            temp_infolist = request.form.get('temp_info')[:-1]
            temp_infolist = temp_infolist.split(",")
            print temp_infolist
            packet_id = request.form.get('packet_id')
            for item in temp_infolist:
                article = Article.query.filter_by(id = item).first()
                if article is not None:
                    article.packet_id = packet_id
                    db.session.add(article)
                    db.session.commit()
                else:
                    flash(u'出现错误')
                    break;
        elif op == 'c_pk':
            packet_name = request.form.get('packet_name')
            packet = Packet(
                packet_name = packet_name
            )
            db.session.add(packet)
            db.session.commit()
            flash(u'分组创建完毕')
    return redirect(url_for('admin.article'))


@admin.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    site_info = site_get()
    article_id = request.args.get('article_id',0)
    temp_dict = {}
    packet_dict = {}
    packet_list = Packet.query.filter_by().all()
    if packet_list is not None:
        for temp in packet_list:
            temp_dict = temp.__dict__
            del temp_dict["_sa_instance_state"]
            packet_dict[str(temp_dict['id'])] = temp_dict['packet_name']
            #packet_dict = dict( packet_dict.items() + tempdict.items() )

    if article_id != 0:
        article = Article.query.filter_by(id = article_id).first()
        #print article
        if article is not None:
            article = article.__dict__
            title = article['title']
            packet_id = article['packet_id']
            show = article['show']
            body = article['body'][:-2]
            
    return render_template('admin/edit.html', **locals())


def gen_rnd_filename():
    filename_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@admin.route('/ckupload/', methods=['GET', 'POST', 'OPTIONS'])
@login_required
def ckupload():
    #site_info = site_get()
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload', rnd_name)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    #print callback
    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@admin.route('/outputjson')
@login_required
def outputjson():
    site_info = site_get()
    tempdict = {}
    tempjson = "["
    info_list = Article.query.filter_by().all()
    for item in info_list:
        tempdict = item.__dict__
        del tempdict["_sa_instance_state"]
        value = json.dumps(tempdict,cls=CJsonEncoder)
        tempjson += value + ",\n"
    tempjson = tempjson[:-2] + "]"
        
    filename = 'page_list_'+str(time.strftime("%Y%m%d"))+'.txt'  
    output = open(filename,'w')  
    output.write(tempjson)  
    output.close()  
    
    flash(u'导出成功，请到根目录查看！')
    return render_template('admin/output.html', **locals())
    
@admin.route('/inputjson')
@login_required
def inputjson():
    site_info = site_get()
       
    filename = 'page_list_'+str(time.strftime("%Y%m%d"))+'.txt'
    output = open(filename,'r')
    for item in json.loads(output.read()):
        print item,item["title"]
        print datetime.strptime(item["timestamp"],'%Y-%m-%d %H:%M:%S')
        #user = User.query.filter_by(username=item["username"]).first()
    
    output.close()  
    
    flash(u'导出成功，请到根目录查看！')
    return render_template('admin/output.html', **locals())
    #return redirect(url_for('main.index'))

