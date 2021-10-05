import sys
sys.path.append('.../venv/Lib/site-packages')
from app.models import *
from . import main
from flask import request, jsonify


#查看学生或老师信息
@main.route('/check', methods=["POST"])
def check():
    get_data = request.get_json()
    sno = get_data['sno']
    s = Student.query.filter_by(sno=sno).first()
    t = Teacher.query.filter_by(sno=sno).first()
    if s and not t:
        infor = {
            "sno": s.sno,
            "name": s.name,
            "classes": s.classes,
            "phone": s.phone,
            "email": s.email
        }
        return jsonify(msg=infor)
    elif t and not s:
        infor = {
            "sno": t.sno,
            "name": t.name,
            "phone": t.phone,
            "email": t.email,
            "office": t.office
        }
        return jsonify(msg=infor)
    else:
        return jsonify(msg='该用户不存在', code=4000)

#根据学号查询信息
@main.route('/check_sno/<sno>', methods=["GET"])
def check_sno(sno):
    s = Student.query.filter_by(sno=sno).first()
    t = Teacher.query.filter_by(sno=sno).first()
    if s and not t:
        infor = {
            "sno": s.sno,
            "name": s.name,
            "classes": s.classes,
            "phone": s.phone,
            "email": s.email
        }
        return jsonify(msg=infor)
    elif t and not s:
        infor = {
            "sno": t.sno,
            "name": t.name,
            "phone": t.phone,
            "email": t.email,
            "office": t.office
        }
        return jsonify(msg=infor, code=200)
    else:
        return jsonify(msg='该用户不存在', code=4000)



######################################
#       待开发区
######################################