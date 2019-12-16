import os
basedir = os.path.abspath(os.path.dirname(__file__))
base_url = '127.0.0.1'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://admin:admin@localhost:5432/myarticles')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisismasecretkey'
    TEST_DATA_Q = int(os.environ.get('TEST_QUANTITY', 100))
    USE_CORE_DB = os.environ.get('USE_SQLALCHEMY_CORE') == 'true'
