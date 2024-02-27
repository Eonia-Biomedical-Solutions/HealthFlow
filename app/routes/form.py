"""
    02/10/2024
    Vista del formulario
"""
import os
import uuid
from app import db
from flask_wtf import FlaskForm
from json import load as jsonload
from flask import (render_template, redirect, flash)

from app.utils import (BuildForm, validate_token)
from . import (routes_bp, PROJECTS_DIR)


@routes_bp.route('/form/<project>', methods=['GET', 'POST'])
async def form(project: str):

    config: dict = {
        'version': '',
        'form_vars': []
    }

    template: str = 'form.html'

    if not validate_token(project_name=project):
        return redirect('/')

    def __validate_project__(project_name: str, _conf_path: str) -> bool:
        return os.path.exists(project_name) and os.path.exists(_conf_path)

    def __load_vars__(conf_file: str):
        config: dict = jsonload(open(conf_file, encoding='utf-8'))

        config['version'] = config.get('version', str(uuid.uuid4()))
        config['form_vars'] = config.get('vars', [])
        if len(config['form_vars']) == 0:
            msg: str = "Se ha detectado un problema con el proyecto actual. Por favor, póngase en contacto con EONIA."
            flash(msg, 'error')
        return config

    _project_path: str = os.path.join(PROJECTS_DIR, project)
    _conf_path: str = os.path.join(PROJECTS_DIR, project, 'config.json')

    if not __validate_project__(_project_path, _conf_path):
        msg: str = "Se ha detectado un problema con el proyecto actual. Por favor, póngase en contacto con EONIA."
        flash(msg, 'error')
        return redirect('/')

    config: dict = __load_vars__(conf_file=_conf_path)
    form: FlaskForm = await BuildForm(config['form_vars'])
    collection_name: str = "{}-{}".format(project, config['version'])

    if form.validate_on_submit():
        form_data = form.data
        form_data.pop('csrf_token')
        _id: str = db.add(collection_name, form_data)
        if len(_id) != 0:
            message: str = "La información se ha guardado exitosamente"
            flash(message, 'success')
        else:
            message: str = "La información no se guardo correctamente."
            flash(message, 'error')
        return redirect(f'/form/{project}')

    return render_template(template, form=form, project=project)
