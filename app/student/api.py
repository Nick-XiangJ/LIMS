import sys
sys.path.append('.../venv/Lib/site-packages')
from . import student
from ..models import *
from flask import jsonify, json, session, request


#登录
@student.route('/login', methods=["POST"])
def login():
    get_data = request.get_json()
    sno = get_data['sno']
    password = get_data['password']
    if not all([sno, password]):
        return jsonify(msg="参数不全", code=4000)
    user = Student.query.filter_by(sno=sno).first()
    if user and user.password == password:
        session["stu_sno"] = sno
        print(sno, password)
        return jsonify(msg="登陆成功", code=200)
    else:
        return jsonify(msg="账号或密码错误", code=4001)

#登录状态
@student.route('/sessions', methods=["GET"])
def sessions():
    sno = session.get("stu_sno")
    if sno:
        return jsonify(msg=sno, code=200)
    else:
        return jsonify(msg="未登录", code=4000)


#退出登录
@student.route('/logout', methods=["DELETE"])
def logout():
    session.clear()
    return jsonify(msg="退出成功", code=200)

#查看自己信息
@student.route('/check', methods=["GET"])
def check():
    sno = session.get("stu_sno")
    if sno:
        s = Student.query.filter_by(sno=sno).first()
        infor = {
            "sno": s.sno,
            "name": s.name,
            "classes": s.classes,
            "phone": s.phone,
            "email": s.email
        }
        return jsonify(msg=infor)
    else:
        return jsonify(msg="请重新登录")


#更新信息内容
"""
    json格式：
        {
            "name":"name",
            "phone":"phone",
            "email":"email",
        }
    """
@student.route('/update', methods=["POST"])
def infor_update():
    sno = session.get('stu_sno')
    get_data = request.get_json()
    if not get_data:
        return jsonify(msg="更新成功", code=200)
    print(sno)
    if sno:
        name = get_data['name']
        phone = get_data['phone']
        email = get_data['email']
        list = []
        if name:
            t = Student.query.filter_by(sno=sno).first()
            t.name = name
            list.append(t)
        if phone:
            t = Student.query.filter_by(sno=sno).first()
            t.phone = phone
            list.append(t)
        if email:
            t = Student.query.filter_by(sno=sno).first()
            t.email = email
            list.append(t)
        try:
            db.session.add_all(list)
            db.session.commit()
            return jsonify(msg='更新成功', code=200)
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(msg="更新失败", code=4000)

#更改密码
"""
    json:
    {
        "new_password":"new_password",
        "password":"password"
    }
"""
@student.route('/changeword', methods=["POST"])
def changeword():
    sno = session.get('stu_sno')
    if sno:
        get_data = request.get_json()
        new_password = get_data['new_password']
        password = get_data['password']
        s = Student.query.filter_by(sno=sno).first()
        if s and s.password == password:
            s.password = new_password
            db.session.add(s)
            db.session.commit()
            return jsonify(msg="修改密码成功", code=200)
        else:
            return jsonify(msg="两次密码不一致", code=4001)
    else:
        return jsonify(msg="请重新登录")

#查看自己课程
@student.route('/courses', methods=["GET"])
def courses():
    sno = session.get('stu_sno')
    list = []
    if sno:
        s = Student.query.filter_by(sno=sno).first()
        for i in s.course:
            for j in i.Teacher:
                infor = {
                    "sno": i.sno,
                    "name": i.name,
                    "start_time": i.start_time,
                    "teacher": j.name
                }
            list.append(infor)
            print(i.sno, i.name, i.start_time)
        return jsonify(msg=list, code=200)
    else:
        return jsonify(msg='未登录', code=4001)







######################################
#       待开发区
######################################

#根据课程表选选修课
@student.route('/uploadcourses', methods=["POST"])
def uploadcourses():
    return jsonify(msg='该功能正在调试', code=4000)
