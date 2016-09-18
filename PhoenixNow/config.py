class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'idontknowwhatthisis'
    SECURITY_PASSWORD_SALT = "fortoken"
    MAIL_DEFAULT_SENDER = "support@phoenixnow.org"

class ProductionConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:pass@db/phoenixrises'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@db/postgres'
    CELERY_BROKER_URL = 'redis://redis:6379/0'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file.db'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
