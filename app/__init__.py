from flask import Flask
from app.utils import MongoDB

db = MongoDB()


def create_app():
    
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
