import sys
sys.path.append('.../venv/Lib/site-packages')
from . import teacher
from ..models import *
from flask import jsonify, json, session, request


#登录
@teacher.route('/login', methods=["POST"])
def login():
    get_data = request.get_json()
    sno = get_data['sno']
    password = get_data['password']
    if not all([sno, password]):
        return jsonify(msg="参数不全", code=4000)
    user = Teacher.query.filter_by(sno=sno).first()
    if user and user.password == password:
        session["teacher_sno"] = sno
        print(sno, password)
        return jsonify(msg="登陆成功", code=200)
    else:
        return jsonify(msg="账号或密码错误", code=4001)

#登录状态
@teacher.route('/sessions', methods=["GET"])
def sessions():
    sno = session.get("teacher_sno")
    if sno:
        return jsonify(msg=sno, code=200)
    else:
        return jsonify(msg="未登录", code=4000)


#退出登录
@teacher.route('/logout', methods=["DELETE"])
def logout():
    session.clear()
    return jsonify(msg="退出成功", code=200)


#查看自己信息
@teacher.route('/check', methods=["GET"])
def check():
    sno = session.get("teacher_sno")
    if sno:
        t = Teacher.query.filter_by(sno=sno).first()
        infor = {
            "sno": t.sno,
            "name": t.name,
            "phone": t.phone,
            "email": t.email,
            "office": t.office
        }
        return jsonify(msg=infor)
    else:
        return jsonify(msg='请重新登录', code=4000)

#更新信息内容
"""
    json格式：
        {
            "name":"name",
            "phone":"phone",
            "email":"email",
            "office":"office"
        }
    """
@teacher.route('/update', methods=["POST"])
def infor_update():
    sno = session.get('teacher_sno')
    get_data = request.get_json()
    if not get_data:
        return jsonify(msg="更新成功", code=200)
    print(sno)
    if sno:
        name = get_data['name']
        phone = get_data['phone']
        email = get_data['email']
        office = get_data['office']
        list = []
        if name:
            t = Teacher.query.filter_by(sno=sno).first()
            t.name = name
            list.append(t)
        if phone:
            t = Teacher.query.filter_by(sno=sno).first()
            t.phone = phone
            list.append(t)
        if email:
            t = Teacher.query.filter_by(sno=sno).first()
            t.email = email
            list.append(t)
        if office:
            t = Teacher.query.filter_by(sno=sno).first()
            t.office = office
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
@teacher.route('/changeword', methods=["POST"])
def changeword():
    sno = session.get('teacher_sno')
    if sno:
        get_data = request.get_json()
        new_password = get_data['new_password']
        password = get_data['password']
        t = Teacher.query.filter_by(sno=sno).first()
        if t and t.password == password:
            t.password = new_password
            db.session.add(t)
            db.session.commit()
            return jsonify(msg="修改密码成功", code=200)
        else:
            return jsonify(msg="旧密码错误，请输入正确密码", code=4001)
    else:
        return jsonify(msg="请重新登录")

#老师给班级发布课程
"""
    json
        {
            "sno":"course_id",
            "name":"course_name",
            "start_time":"time"
            "classes":"classes"
            "end_time":"默认 start_time + 2h"
        }
"""
@teacher.route('/uploadcourse', methods=["POST"])
def uploadcourse():
    t_sno = session.get("teacher_sno")
    if t_sno:
        get_data = request.get_json()
        c_sno = get_data['sno']
        c_name = get_data['name']
        c_start_time = get_data['start_time']
        classes = get_data['classes']
        if not all([c_sno, c_name, c_start_time, classes]):
            return jsonify(msg="参数不全", code=4001)
        c1 = Course.query.filter_by(sno=c_sno).first()
        if c1:
            return jsonify(msg="课程编号已存在", code=4000)
        else:
            try:
                c = Course(sno=c_sno, name=c_name, start_time=c_start_time)
                db.session.add(c)
                db.session.commit()
                t = Teacher.query.filter_by(sno=t_sno).first()
                c = Course.query.filter_by(sno=c_sno).all()
                for c1 in c:
                    t.course.append(c1)
                    db.session.add(t)
                    db.session.commit()
                stu = Student.query.filter_by(classes=classes).all()
                for s in stu:
                    for c1 in c:
                        s.course.append(c1)
                        db.session.add(t)
                        db.session.commit()
                return jsonify(msg="课程加入成功", code=200)
            except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify(msg='插入数据库失败', code=4000)
    else:
        return jsonify(msg='未登录', code=4001)


#老师查看自己课程或者查看课程对应学生
@teacher.route('/courses', methods=["GET"])
def courses():
    t_sno = session.get("teacher_sno")
    list = []
    if t_sno:
        t = Teacher.query.filter_by(sno=t_sno).first()
        for i in t.course:
            student = []
            for j in i.Student:
                students = {
                    "sno": j.sno,
                    "name": j.name
                }
                student.append(students)
            infor = {
                "sno": i.sno,
                "name": i.name,
                "start_time": i.start_time,
                "students": student
            }
            list.append(infor)
            print(i.sno, i.name, i.start_time)
        return jsonify(msg=list, code=200)
    else:
        return jsonify(msg='未登录', code=4001)

"""
    {
        "sno":"用品唯一标识",
        "name":"用品名称"
    }
"""
#老师单次导入实验用品数据
@teacher.route('/add_tool', methods=["POST"])
def add():
    t_sno = session.get('teacher_sno')
    if t_sno:
        get_data = request.get_json()
        sno = get_data['sno']
        name = get_data['name']
        print(sno, name)
        tool = Tools.query.filter_by(sno=sno).first()
        if tool:
           return jsonify(msg='该用品唯一标识已存在', code=4000)
        try:
            t = Tools(sno=sno, name=name)
            db.session.add(t)
            db.session.commit()
            return jsonify(msg='导入成功', code=200)
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(msg='导入失败', code=4001)
    else:
        return jsonify(msg='请重新登录', code=4001)








######################################
#       待开发区
######################################



"""
    json
    {
        "sno":"course_id",
        "name":"course_name",
        "start_time":"time"
        "end_time":"默认 start_time + 2h"
    }
"""
#老师发布课程，类似选修课，学生自行添加
@teacher.route('/uploadcourses', methods=["POST"])
def uploadcourses():
    return jsonify(msg='该功能正在调试', code=4000)