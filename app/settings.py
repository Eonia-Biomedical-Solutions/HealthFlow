from os import environ

DEV_MODE = environ.get('FLASK_ENV', 'production') == 'development'
SECRET_KEY = environ.get('SECRET_KEY', 'e4c61a2fcbfe245b8d8b763ec3860bd2257b31145c71f1e5')
DATABASE = environ.get('DATABASE', 'HealthFlow')

if DEV_MODE:
    MONGO_URI = 'mongodb://localhost:27017'
else:
    MONGO_URI = environ.get('MONGO_URI')
