import os
import jwt
import datetime
from json import load as jsonload
from flask import (request, render_template, flash, redirect, make_response,
                   current_app)
from . import (routes_bp, PROJECTS_DIR)


@routes_bp.route('/login/<project>', methods=['GET', 'POST'])
def login(project: str):
    template = 'login.html'

    def __validate_project__(project_name: str, _conf_path: str) -> bool:
        return os.path.exists(project_name) and os.path.exists(_conf_path)

    def __load_vars__(conf_file: str):
        config: dict = jsonload(open(conf_file, encoding='utf-8'))
        config['usr'] = config.get('usr', '')
        config['pssw'] = config.get('pssw', '')

        if len(config['usr']) == 0 or len(config['pssw']) == 0:
            msg:str = f"Se ha detectado un problema con el proyecto {project}. Por favor, póngase en contacto con EONIA "
            flash(msg, 'error')
        return config

    _project_path: str = os.path.join(PROJECTS_DIR, project)
    _conf_path: str = os.path.join(PROJECTS_DIR, project, 'config.json')

    if not __validate_project__(_project_path, _conf_path):
        msg:str = f"Se ha detectado un problema con el proyecto {project}. Por favor, póngase en contacto con EONIA "
        flash(msg, 'error')
        return redirect('/')

    if request.method == 'POST':
        config: dict = __load_vars__(conf_file=_conf_path)

        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == config['usr'] and password == config['pssw']:
            token = jwt.encode({
                'project': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            },
                current_app.config['SECRET_KEY'], algorithm='HS256')
            response = make_response(redirect(f'/form/{project}'))
            response.set_cookie('token', token)
            return response

        else:
            msg: str = f"El usuario o contraseña no son válidos."
            flash(msg, 'error')
            return render_template(template, project=project)

    return render_template(template, project=project)
