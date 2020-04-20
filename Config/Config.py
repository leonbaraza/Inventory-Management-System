# import secrets

class Config():
    DEBUG = True
    SECRET_KEY = 'dsgvsdfsdvndvndfnkvsdfvsxsvndfvndfvndfvnwe12ss'
    # SECRET_KEY = secrets.token_hex(16)

class Development(Config):
    # database://user:password@host:port/databasename
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:L@127.0.0.1:5432/test'


class Production(Config):
    pass

