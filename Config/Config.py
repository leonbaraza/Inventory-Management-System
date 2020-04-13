
class Config():
    DEBUG = True
    SECRET_KEY = 'dsgvsdfsdvndvndfnkvsdfvsxsvndfvndfvndfvnwe12ss'

class Development(Config):
    # database://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@127.0.0.1:5432/test'


class Production():
    pass

