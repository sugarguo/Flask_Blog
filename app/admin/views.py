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
from ..models import User, Article
from manage import app


work_statuslist = {
               "0" : u"组长",
               "1" : u"员工"
               }

submit_statuslist = {
               "0" : u"未提交",
               "1" : u"已提交"
               }


@admin.route('/login', methods = ['GET', 'POST'])
def login():
    titlename = u"Sugarguo_Flask_Blog"
    if request.method == 'POST':
        username=request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user.work_status == 0 or username == 'admin':
            if user is not None and user.verify_password(password = request.form.get('password')):
                login_user(user, request.form.get('remember_me'))
                return redirect(request.args.get('next') or url_for('admin.control'))
            flash(u'用户名或密码错误，请重试！')
        else:
            flash(u'普通用户禁止登陆！请使用管理员用户登陆！')
    return render_template('admin/login.html', **locals())

@admin.route('/logout')
@login_required
def logout():
    titlename = u"Sugarguo_Flask_Blog"
    logout_user()
    flash(u'你已经退出系统！')
    return redirect(url_for('main.index'))

@admin.route('/test')
@login_required
def test():
    titlename = u"Sugarguo_Flask_Blog"
    return "adsdsa"


def getinfo_TeamName(team_id):
    tempdict = {}
    tempname = ""
    teamteamlist = Team.query.filter_by(id = team_id).first()
    if teamteamlist is not None:
        tempdict = teamteamlist.__dict__
        return tempdict['name']
    
def getinfo_TeamLeader(team_id):
    tempdict = {}
    tempname = ""
    teamteamlist = Team.query.filter_by(id = team_id).first()
    if teamteamlist is not None:
        tempdict = teamteamlist.__dict__
        return tempdict['leader_id']
    
        
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


@admin.route('/getinfo/control', methods = ['GET', 'POST'])
@login_required
def getinfo_control():
    tempdict = {}
    userlist = []
    tempjson = "["
    if current_user.username == u'admin':
        userlist = db.session.query(User).filter(User.username != 'admin').all()
        #print "admin",userlist
    else:
        leaderlist = Team.query.filter_by(leader_id = request.args.get('user_id',0)).all()
        if leaderlist is not None:
            for team_id in leaderlist:
                #team_id.__dict__['id']
                userlist = userlist + User.query.filter_by(team_id = team_id.__dict__['id']).all()
            userlist = userlist + db.session.query(User).filter(User.team_id == None, User.work_status != 0).all()
            #User.query.filter_by(team_id = None).all()
        #userlist = User.query.filter_by(team_id = team_id).all()
    if userlist is not None:
        for item in userlist:
            #print item
            #item.workload = str(item.workload)
            #item.endtime = item.endtime.strftime("%Y-%m-%d %H:%M:%S")
            tempdict = item.__dict__
            del tempdict["_sa_instance_state"]
            #print tempdict
        
            tempdict['teamname'] = getinfo_TeamName(tempdict['team_id'])
            value = json.dumps(tempdict,cls=CJsonEncoder)
            tempjson += value + ","
        tempjson = tempjson[:-1] + "]"

    #print tempjson
    return tempjson



@admin.route('/show')
@login_required
def show():
    titlename = u"Sugarguo_Flask_Blog"
    #print current_user
    #print current_user.is_authenticated()
    return render_template('admin/show.html', **locals())



@admin.route('/control')
@login_required
def control():
    titlename = u"Sugarguo_Flask_Blog"
    
    teamdict = {}
    userdict = {}
    tempdict = {}
    #teamdict['0'] = 'null'
    
    #print current_user.username
    if current_user.username == u'admin':
        team_id = -1
        teamlist = Team.query.filter_by().all()
        userlist = db.session.query(User).filter(User.username != 'admin').all()
        if teamlist is not None:
            for item in teamlist:
                tempdict = item.__dict__
                teamdict[str(tempdict['id'])] = tempdict['name']
        if userlist is not None:
            for item in userlist:
                tempdict = item.__dict__
                userdict[str(tempdict['id'])] = tempdict['username']
    else:
        user = User.query.filter_by(username=current_user.username).first()
        if user is not None:
        #print user.__dict__
            team_id = user.__dict__['team_id']
            user_id = user.__dict__['id']
            if team_id == None:
                team_id = -1
            teamlist = Team.query.filter_by(leader_id = int(user.__dict__['id'])).all()
            if teamlist is not None:
                for item in teamlist:
                    tempdict = item.__dict__
                    teamdict[str(tempdict['id'])] = tempdict['name']
                #print teamlist
            userdict[int(user.__dict__['id'])] = user.__dict__['username']
        #userlist = User.query.filter_by(team_id = team_id).all()
    #print current_user
    #team_id = int(request.args.get('team_id',0))
    #user_role = Team.query.filter_by(name="first").first()
    #users = user_role.users
    worklist = work_statuslist
    submitlist = submit_statuslist
    #users[0].role
    
    #query = User.query.filter_by().all()
    #print query
    #print query[0].role
    #print dir(data[0])
    #print data[0].Test.name
    #print current_user.is_authenticated()
    return render_template('admin/control.html', **locals())


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


@admin.route('/sendmail')
@login_required
def sendmail():
    titlename = u"Sugarguo_Flask_Blog"
    send_email('wang.chao@embedway.com', 'Confirm Your Account',
               'admin/email/confirm', sendstr='send ok')
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
    #print current_user
    #print current_user.is_authenticated()
    #return render_template('admin/control.html', **locals())