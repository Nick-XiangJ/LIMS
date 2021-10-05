import sys
sys.path.append('./venv/Lib/site-packages')
from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app("develop")
manager = Manager(app)
Migrate(app, db)

manager.add_command("db", MigrateCommand)  #绑定额外的db命令

"""
额外命令如下
python3 manage.py db init #初始化
python3 manage.py db migrate -m "init message" #提交变更
python3 manage.py db upgrade # 升级变更
python3 manage.py db downgrade # 降级变更
"""
if __name__ == '__main__':
    manager.run()