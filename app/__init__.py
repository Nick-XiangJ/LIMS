import sys
sys.path.append('../venv/Lib/site-packages')
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from config import config_map, redis_store
import pymysql

#创建一个无参数据库对象

db = SQLAlchemy()

def create_app(dev_name):  #dev_name 为配置对象
    app = Flask(__name__)
    config_class = config_map.get(dev_name)
    app.config.from_object(config_class) #从类中读取信息

    db.init_app(app) #实例化数据库对象

    Session(app) #将session数据保存到redis中

    #注册蓝图

    from app import admin, main, student, teacher

    app.register_blueprint(main.main, url_prefix="/main")
    app.register_blueprint(admin.admin, url_prefix="/admin")
    app.register_blueprint(student.student, url_prefix="/student")
    app.register_blueprint(teacher.teacher, url_prefix="/teacher")

    return app