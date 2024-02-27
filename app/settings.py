from os import environ

DEV_MODE = environ.get('FLASK_ENV', 'production') == 'development'
SECRET_KEY = environ.get('SECRET_KEY')
DATABASE = environ.get('DATABASE')

if DEV_MODE:
    MONGO_URI = 'mongodb://localhost:27017'
else:
    MONGO_URI = environ.get('MONGO_URI')