from secrets import token_hex

from os import getenv


"""

The database credentials
should be created at a .env file and pass here.

"""

class Config(object):
    
    SECRET_KEY = token_hex(32)

    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")



