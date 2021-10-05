import sys
sys.path.append('.../venv/Lib/site-packages')
from app.models import *
from flask import request, jsonify, session
from . import admin

#登录
@admin.route('/login', methods=["POST"])
def login():
    get_data = request.get_json()
    sno = get_data['sno']
    password = get_data['password']
    if not all([sno, password]):
        return jsonify(msg="参数不全", code=4000)
    user = Admin.query.filter_by(sno=sno).first()
    if user and user.password == password:
        session["admin_sno"] = sno
        print(sno, password)
        return jsonify(msg="登陆成功", code=200)
    else:
        return jsonify(msg="账号或密码错误", code=4001)


#登录状态
@admin.route('/sessions', methods=["GET"])
def sessions():
    sno = session.get("admin_sno")
    if sno:
        return jsonify(msg=sno, code=200)
    else:
        return jsonify(msg="未登录", code=4000)


#退出登录
@admin.route('/logout', methods=["DELETE"])
def logout():
    session.clear()
    return jsonify(msg="退出成功", code=200)


#单条信息注入

@admin.route('/insert_stu', methods=["POST"])
def insert_stu():
    get_data = request.get_json()
    sno = get_data['sno']
    name = get_data['name']
    classes = get_data['classes']
    phone = get_data['phone']
    email = get_data['email']
    if not all([sno, name, classes]):
        return jsonify(msg="参数不全", code=4001)
    try:
        s = Student(sno=sno, name=name, classes=classes, phone=phone, email=email)
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="插入成功", code=200)
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(msg='数据库插入错误', code=4000)

@admin.route('/insert_teacher', methods=["POST"])
def insert_teacher():
    get_data = request.get_json()
    sno = get_data['sno']
    name = get_data['name']
    phone = get_data['phone']
    email = get_data['email']
    office = get_data['office']
    if not all([sno, name]):
        return jsonify(msg='参数不全', code=4001)
    try:
        s = Teacher(sno=sno, name=name, phone=phone, email=email, office=office)
        db.session.add(s)
        db.session.commit()
        return jsonify(msg="插入成功", code=200)
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(msg='数据库插入失败', code=4000)

#批量导入学生
#默认接受json格式为：
"""
{
    "raws":[{
        "sno":"01",
        "name":"nn",
        "classes":"06051701"
    },
    {
        "sno":"01",
        "name":"nn",
        "classes":"06051701"
    }],
    "sum":"2"
}
"""
@admin.route('/insert_manystu', methods=["POST"])
def insert_manystu():
    get_data = request.get_json()
    raws = get_data["raws"]
    sum = get_data['sum']
    students = []
    for i in range(0, int(sum)):
        get_data = raws[i]
        sno = get_data['sno']
        name = get_data['name']
        classes = get_data['classes']
        if not all([sno, name, classes]):
            return jsonify(msg="参数不全", code=4001)
        s = Student(sno=sno, name=name, classes=classes)
        students.append(s)
    try:
        db.session.add_all(students)
        db.session.commit()
        return jsonify(msg='批量导入成功', code=200)
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(msg="导入失败", code=4000)


@admin.route('/insert_manyteacher', methods=["POST"])
def insert_manyteacher():
    get_data = request.get_json()
    raws = get_data["raws"]
    sum = get_data['sum']
    teacher = []
    for i in range(0, int(sum)):
        get_data = raws[i]
        sno = get_data['sno']
        name = get_data['name']

        if not all([sno, name]):
            return jsonify(msg="参数不全", code=4001)
        t = Teacher(sno=sno, name=name)
        teacher.append(t)
    try:
        db.session.add_all(teacher)
        db.session.commit()
        return jsonify(msg='批量导入成功', code=200)
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(msg="导入失败", code=4000)

#删除某条信息
"""
    {
        "postion":"Student/Teacher"
        "sno":"sno"    
    }
"""
@admin.route('/delete', methods=["POST"])
def deleteinfor():
    sno = session.get('admin_sno')
    if sno:
        get_data = request.get_json()
        pos = get_data['postion']
        sno = get_data['sno']
        if pos == "Student" or pos == "student":
            s = Student.query.filter_by(sno=sno).first()
            if s:
                db.session.delete(s)
                db.session.commit()
                return jsonify(msg='删除成功', code=200)
            else:
                return jsonify(msg='用户不存在', code=4001)
        else:
            t = Teacher.query.filter_by(sno=sno).first()
            if t:
                db.session.delete(t)
                db.session.commit()
                return jsonify(msg='删除成功', code=200)
            else:
                return jsonify(msg='用户不存在', code=4001)
    else:
        return jsonify(msg="请重新登录", code=4000)













#多条信息删除
@admin.route('/delete_many', methods=["POST"])
def delete_many():
    return jsonify(msg='该功能正在调试', code=4000)