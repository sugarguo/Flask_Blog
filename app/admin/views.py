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
from datetime import datetime, date

from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_user, login_required, logout_user, current_user

from . import admin
from .. import db
from ..models import User, Article, Packet
from manage import app


show_list = {
               "0" : u"不显示",
               "1" : u"显示"
               }


@admin.route('/login', methods = ['GET', 'POST'])
def login():
    titlename = u"Sugarguo_Flask_Blog"
    if request.method == 'POST':
        username=request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password = request.form.get('password')):
            login_user(user, request.form.get('remember_me'))
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash(u'用户名或密码错误，请重试！')
    return render_template('admin/login.html', **locals())

@admin.route('/logout')
@login_required
def logout():
    titlename = u"Sugarguo_Flask_Blog"
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
    titlename = u"Sugarguo_Flask_Blog"
    site_name = u"糖果果技术博客"
    #print current_user
    #print current_user.is_authenticated()
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
    titlename = u"Sugarguo_Flask_Blog"
    
    global show_list
    show_dict = show_list
    #print current_user
    #print current_user.is_authenticated()
    return render_template('admin/article.html', **locals())
    

@admin.route('/psotarticle', methods = ['GET', 'POST'])
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
                article.title = request.form.get('title'),
                article.packet_id = request.form.get('packet_id'),
                article.show = request.form.get('show'),
                article.body = request.form.get('body'),
                article.timestamp = datetime.now()
                db.session.add(article)
                db.session.commit()
            flash(u'文章更新完毕')
            
    return redirect(url_for('admin.article'))



@admin.route('/delete', methods = ['GET', 'POST'])
@login_required
def delete_article():
    article_id = request.args.get('article_id',-1)
    print article_id
    article = Article.query.filter_by(id = article_id).first()
    print article
    if article is not None:
        print "enter"
        db.session.delete(article)
        db.session.commit()
    flash(u'文章删除完毕')
            
    return redirect(url_for('admin.article'))


@admin.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    titlename = u"Sugarguo_Flask_Blog"
    article_id = request.args.get('article_id',0)
    body = u"巴拉巴拉"
    tempdict = {}
    packet_dict = {}
    packet_list = Packet.query.filter_by().all()
    if packet_list is not None:
        for temp in tempdict:
            tempdict = temp.__dict__
            del tempdict["_sa_instance_state"]
            packet_dict = dict( packet_dict.items() + tempdict.items() )

    if article_id != 0:
        article = Article.query.filter_by(id = article_id).first()
        print article
        if article is not None:
            article = article.__dict__
            title = article['title']
            packet_id = article['packet_id']
            show = article['show']
            body = article['body'][:-1]
            
    return render_template('admin/edit.html', **locals())


@admin.route('/ckupload/', methods=['POST', 'OPTIONS'])
@login_required
def ckupload():
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

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@admin.route('/outputjson')
@login_required
def outputjson():
    titlename = u"Sugarguo_Flask_Blog"
    tempdict = {}
    tempjson = "["
    recordinglist = db.session.query(User.username, Recording).filter(User.id == Recording.user_id, 'YEARWEEK(`endtime`) = YEARWEEK(now())-1').all()
    for item in recordinglist:
        tempdict = item[1].__dict__
        del tempdict["_sa_instance_state"]
        del tempdict["user_id"]
        tempdict["username"] = item[0]
        tempdict["shortsha1"] = "embedway"
        tempdict["link"] = "sugarguo"
        value = json.dumps(tempdict,cls=CJsonEncoder)
        tempjson += value + ",\n"
    tempjson = tempjson[:-2] + "]"
        
    filename = 'page_list_'+str(time.strftime("%Y%m%d"))+'.txt'  
    output = open(filename,'w')  
    output.write(tempjson)  
    output.close()  
    
    flash(u'导出成功，请到根目录查看！')
    return render_template('admin/output.html', **locals())
    #return redirect(url_for('main.index'))
    
@admin.route('/inputjson')
@login_required
def inputjson():
    titlename = u"Sugarguo_Flask_Blog"
       
    filename = 'page_list_'+str(time.strftime("%Y%m%d"))+'.txt'
    output = open(filename,'r')
    for item in json.loads(output.read()):
        print item,item["username"]
        print datetime.strptime(item["endtime"],'%Y-%m-%d')
        #user = User.query.filter_by(username=item["username"]).first()
    
    output.close()  
    
    flash(u'导出成功，请到根目录查看！')
    return render_template('admin/output.html', **locals())
    #return redirect(url_for('main.index'))
