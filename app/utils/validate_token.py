import jwt
from os import environ
from flask import request, flash
from flask import current_app as app


def validate_token(project_name: str):
    token = request.cookies.get('token')

    if not token:
        flash('Por favor, inicia sesión en tu proyecto.', 'error')
        return False
    try:
        data: dict = jwt.decode(token, app.config['SECRET_KEY'],
                                algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'error')
        return False
    except jwt.InvalidTokenError:
        flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'error')
        return False

    return data['project'] == project_name
