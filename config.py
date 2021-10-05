import sys
sys.path.append('./venv/Lib/site-packages')
import redis
redis_store = redis.Redis(host='127.0.0.1', port=6379, db=1)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "sdfsdfsdf"

    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 600 #生命周期,单位s


#开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:981121@127.0.0.1:3306/bishe_test'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, password="jamkung", db=2)  # 操作的redis配置
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=2)  # 操作的redis配置
    DEBUG = True

#线上环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:981121@120.79.182.119:3306/bishe_test'
    SESSION_REDIS = redis.Redis(host='120.79.182.119', port=6379, password="", db=3)  # 操作的redis配置


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}