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
from ..models import User, Article



downlist={
        "1":u"产品手册","2":u"代码评审","3":u"功能测试","4":u"回归测试",
        "5":u"外部测试","6":u"学习","7":u"外部支持","8":u"性能测试","9":u"测试调试",
        "10":u"用例设计","11":u"系统测试","12":u"编程自测","13":u"设计文档","14":u"设计评审",
        "15":u"评估立项","16":u"说明文档","17":u"内部支持","18":u"部门相关","19":u"配置管理文档",
        "20":u"需求分析","21":u"会议","22":u"培训","23":u"指导","24":u"请假","25":u"其他",
        "26":u"节假日","28":u"单元测试","29":u"功能预研","30":u"概要/详细设计","31":u"编码实现"
        }



def getinfo_TeamName(team_id):
    tempdict = {}
    tempname = ""
    teamteamlist = Team.query.filter_by(id = team_id).first()
    if teamteamlist is not None:
        tempdict = teamteamlist.__dict__
        return tempdict['name']

def getinfo_TeamUserList(team_id):
    tempdict = {}
    tempname = ""
    teamuserlist = User.query.filter_by(team_id = team_id).all()
    if teamuserlist is not None:
        for item in teamuserlist:
            tempdict = item.__dict__
            #print tempdict['username']
            tempname += tempdict['username'] + ','
        return tempname[:-1]


@main.route('/getinfo/team', methods = ['GET', 'POST'])
def getinfo_team():
    tempdict = {}
    tempjson = "["
    #projectlist = Recording.query.filter_by(id = userid).all()
    teamlist = Team.query.filter_by().all()
    #user = User.query.filter_by(username = form.username.data).first()
    for item in teamlist:
        tempdict = item.__dict__
        tempdict['teamlist'] = getinfo_TeamUserList(tempdict['id'])
        queryname = User.query.filter_by(id = tempdict['leader_id']).first()
        if queryname is None:
            tempdict['team_leader'] = 'null'
        else:
            queryname = queryname.__dict__
            tempdict['team_leader'] = queryname['username']
        del tempdict["_sa_instance_state"]
        value = json.dumps(tempdict)
        tempjson += value + ","
    tempjson = tempjson[:-1] + "]"

    #print tempjson
    return tempjson


@main.route('/getinfo/userlist', methods = ['GET', 'POST'])
def getinfo_userlist():
    #print request.args.get()
    teamid=int(request.args.get('team_id',0))
    #teamid = request.args.get()
    tempdict = {}
    tempjson = "["
    #projectlist = Recording.query.filter_by(id = userid).all()
    userlist = User.query.filter_by(team_id = teamid).all()
    #print teamid,userlist
    #userlist = User.query.filter_by().all()
    #user = User.query.filter_by(username = form.username.data).first()
    if userlist is not None:
        for item in userlist:
            tempdict = item.__dict__
            del tempdict["_sa_instance_state"]
            value = json.dumps(tempdict)
            tempjson += value + ","
        tempjson = tempjson[:-1] + "]"

    #print tempjson
    return tempjson


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



@main.route('/getinfo/user', methods = ['GET', 'POST'])
def getinfo_recordinguserlist():

    userid = request.args.get('user_id',0)

    tempdict = {}
    tempjson = "["

    #recordinglist = db.session.query(Recording).filter('(YEARWEEK(`endtime`) = YEARWEEK(now())-1 or YEARWEEK(`endtime`) = YEARWEEK(now())) and `user_id` =' + userid).all()
    recordinglist = db.session.query(Recording).filter(Recording.user_id == userid , \
            'YEARWEEK(`endtime`) = YEARWEEK(now())-1'\
            ).all()
    for item in recordinglist:
        tempdict = item.__dict__
        del tempdict["_sa_instance_state"]
        value = json.dumps(tempdict,cls=CJsonEncoder)
        tempjson += value + ","
        #tempjson = tempjson[:-2] + "]"
        #value = json.dumps(tempdict,cls=CJsonEncoder)
        #tempjson += value + ","
    tempjson = tempjson[:-1] + "]"

    #print tempjson
    return tempjson



@main.route('/')
@main.route('/index.html')
def index():
    titlename = u"Sugarguo_Flask_Blog"
    teamdict = {}
    tempdict = {}
    userdict = {}
    teamlist = db.session.query(User.username, Team).filter(User.id == Team.leader_id).all()#teamlist = Team.query.filter_by().all()
    if teamlist is not None:
        for item in teamlist:
            tempdict = item[1].__dict__
            del tempdict["_sa_instance_state"]
            teamdict[str(tempdict['id'])] = tempdict['name'] + ' | ' + item[0]
    userlist = db.session.query(User).filter(User.username != 'admin').all()#User.query.filter_by().all()
    if userlist is not None:
        for item in userlist:
            tempdict = item.__dict__
            userdict[str(tempdict['id'])] = tempdict['username']
    return render_template('index.html', **locals())


@main.route('/team')
@main.route('/team.html')
def team():
    titlename = u"Sugarguo_Flask_Blog"
    #print request.args.get('team_id',0)
    team_id = request.args.get('team_id',0)
    teamdict = {}
    tempdict = {}
    userdict = {}
    teamlist = db.session.query(User.username, Team).filter(User.id == Team.leader_id).all()#Team.query.filter_by().all()
    if teamlist is not None:
        for item in teamlist:
            tempdict = item[1].__dict__
            del tempdict["_sa_instance_state"]
            teamdict[str(tempdict['id'])] = tempdict['name'] + ' | ' + item[0]
    userlist = User.query.filter_by(team_id=team_id).all()
    if userlist is not None:
        for item in userlist:
            tempdict = item.__dict__
            userdict[str(tempdict['id'])] = tempdict['username']
    return render_template('team.html', **locals())

@main.route('/test')
@main.route('/test.html')
def test():
    titlename = u"Sugarguo_Flask_Blog"
    #print request.args.get('user_id',0)
    user_id = request.args.get('user_id',0)
    return render_template('test.html', **locals())


@main.route('/user')
@main.route('/user.html')
def user():
    titlename = u"Sugarguo_Flask_Blog"
    dlist = downlist
    #print request.args.get('user_id',0)
    user_id = request.args.get('user_id',0)
    show = request.args.get('show','true')
    user = User.query.filter_by(id = user_id).first()
    if user is not None:
        username = user.__dict__['username']
    else:
        username = 'None'
    team_id = request.args.get('team_id',0)
    return render_template('user.html', **locals())



@main.route('/user/infodo', methods = ['GET', 'POST'])
def infodo():
    #print request.args.get('user_id',0)
    if request.method == 'POST':
        op = request.form.get('op')
        user_id = request.args.get('user_id',0)
        id = request.form.get('id')
        if op == "modify":
            recording = Recording.query.filter_by(id = id,user_id = user_id).first()
            recording.workload = request.form.get('workload')
            recording.workcontent = request.form.get('workcontent')
            db.session.add(recording)
            db.session.commit()
            flash(u'数据更新完毕')
        elif op == "create":
            recordings = Recording(id = id,
                    project=request.form.get('project'),
                    branch = request.form.get('branch'),
                    endtime = request.form.get('endtime'),
                    worktype = request.form.get('worktype'),
                    workload = request.form.get('workload'),
                    workcontent = request.form.get('workcontent'),
                    user_id = request.args.get('user_id',0)
                    )
            #db.session.merge(recordings)
            db.session.add(recordings)
            db.session.commit()
            flash(u'数据创建完毕')
        elif op == "delete":
            #print "delete"
            recording = Recording.query.filter_by(id = id,user_id = user_id).first()
            db.session.delete(recording)
            db.session.commit()
            flash(u'数据删除完毕')
        return redirect("/user?user_id=" + user_id)
    #response = make_response("/user?user_id=" + user_id)
    #return response   
    #return redirect(request.args.get('next'))
        #return redirect(url_for('main.uS'))
    return render_template('user.html')# ,form=form)



@main.route('/user/submit', methods = ['GET', 'POST'])
def infosubmit():
    #print request.args.get('user_id',0)
    user_id = request.args.get('user_id',0)
    user = User.query.filter_by(id = user_id).first()
    if user is not None:
        user.submit_status = 1
        db.session.add(user)
        db.session.commit()
        flash(u'数据提交完毕')
    else:
        flash(u'出现错误，用户未找到请检查后重试！')        
    return redirect("/user?user_id=" + user_id)


@main.route('/admin/infodo', methods = ['GET', 'POST'])
def admindo():
    #print request.args.get('user_id',0)
    if request.method == 'POST':
        op = request.form.get('op')
        type = request.form.get('type')
        user_id = request.args.get('user_id',0)
        id = request.form.get('id')
        if type == "team":
            if op == "modify":
                team = Team.query.filter_by(id = request.form.get('team_id')).first()
                team.name = request.form.get('name')
                team.leader_id = request.form.get('leader_id')
                db.session.add(team)
                db.session.commit()
                flash(u'数据更新完毕')
            elif op == "create":
                team = Team(id = request.form.get('team_id'),
                        name = request.form.get('name'),
                        leader_id = request.form.get('leader_id')                            
                        )
                #user = User.query.filter_by(id = request.form.get('leader_id')).first()
                #user.team_id = request.form.get('team_id')
                #db.session.add(user)
                db.session.add(team)
                db.session.commit()
                flash(u'数据更新完毕')
            elif op == "delete":
                team = Team.query.filter_by(id = request.form.get('team_id')).first()
                db.session.delete(team)
                db.session.commit()
                flash(u'数据删除完毕')                
        elif type == "user":
            if op == "modify":
                user = User.query.filter_by(id = request.form.get('id')).first()
                team = Team.query.filter_by(leader_id = request.form.get('id')).all()
                if team is not None:
                    for item in team:
                        item.leader_id = request.form.get('user_id')
                        db.session.add(item)
                record = Recording.query.filter_by(user_id = request.form.get('id')).all()
                if record is not None:
                    for item in team:
                        item.user_id = request.form.get('user_id')
                        db.session.add(item)
                db.session.commit()
                user.password = request.form.get('user_password')
                user.id = request.form.get('user_id')
                user.username = request.form.get('user_name')
                user.team_id = request.form.get('team_id')
                user.email = request.form.get('user_email')
                user.work_status = request.form.get('work_status')
                db.session.add(user)
                db.session.commit()
                flash(u'数据更新完毕')
            elif op == "create":
                user = User.query.filter_by(id = request.form.get('user_id')).first()
                if user is not None:
                    flash(u'请检查工号，不能重复！')
                else:
                    if request.form.get('team_id') == "":
                        user = User(id = request.form.get('user_id'),
                                username = request.form.get('user_name'),
                                password = request.form.get('user_password'),
                                email = request.form.get('user_email'),
                                work_status = request.form.get('work_status')                          
                                )
                    else:
                        user = User(id = request.form.get('user_id'),
                                username = request.form.get('user_name'),
                                password = request.form.get('user_password'),
                                email = request.form.get('user_email'),
                                work_status = request.form.get('work_status'),
                                team_id = request.form.get('team_id')                            
                                )
                        db.session.add(user)
                    db.session.commit()
                    flash(u'数据更新完毕')
            elif op == "delete":
                user = User.query.filter_by(id = request.form.get('id')).first()
                if current_user.username == 'admin':
                    recording = Recording.query.filter_by(user_id = request.form.get('id')).all()
                    for record in recording:
                        db.session.delete(record)
                    db.session.delete(user)
                else:
                    user.team_id = None
                    db.session.add(user)
                db.session.commit()
                flash(u'数据删除完毕')                
        return redirect(url_for('admin.control'))
    return render_template('admin/control.html')


@main.route('/admin/infocd', methods = ['GET', 'POST'])
def admincd():
    team_id = request.form.get('team_id')
    cd_chk = request.form.get('cd_chk')[:-1]
    cd_chklist = cd_chk.split(",")
    if request.method == 'POST':
        op = request.form.get('op')
        if op == "modify":
            for item in cd_chklist:
                user = User.query.filter_by(id = item).first()
                if user is not None:
                    user.team_id = team_id
                    db.session.add(user)
                    db.session.commit()
                else:
                    flash(u'出现错误')
                    break;
            flash(u'数据更新完毕')
        elif op == "deleteu":
            for item in cd_chklist:
                user = User.query.filter_by(id = item).first()
                db.session.delete(user)
                db.session.commit()
            flash(u'用户数据删除完毕')
        elif op == "deletet":
            team = Team.query.filter_by(id = team_id).first()
            db.session.delete(team)
            db.session.commit()
            flash(u'用户数据删除完毕')
        return redirect(url_for('admin.control'))
    return render_template('admin/control.html')
