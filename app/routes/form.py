"""
    02/10/2024
    Vista del formulario
"""
import os
import uuid
from flask_wtf import FlaskForm
from json import load as jsonload
from flask import (render_template, redirect, flash)

from app.utils import (DataBase, BuildForm)
from . import (routes_bp, PROJECTS_DIR)


@routes_bp.route('/form/<project>', methods=['GET', 'POST'])
async def form(project: str):
    """Vista dinamica de formulario
    Args:
        project (str): folder a un proyecto activo
    """

    config: dict = {
        'db_file': '',
        'version': '',
        'form_vars': []
    }

    template: str = 'form.html'

    def __validate_project__(project_name: str, _conf_path: str) -> bool:
        """Valida que el proyecto tenga los archivos necesarios para funcionar_
        """
        return os.path.exists(project_name) and os.path.exists(_conf_path)

    def __load_vars__(conf_file: str):
        """Carga las variables en config, en dado caso que no existan, se agrega a default
        si la longitud de variables es 0, debe retornar un modal
        """
        config: dict = jsonload(open(conf_file, encoding='utf-8'))
        config['db_file'] = os.path.join(PROJECTS_DIR, project,
                                         config.get('db_file',
                                                    'db.db'))
        config['version'] = config.get('version', str(uuid.uuid4()))
        config['form_vars'] = config.get('vars', [])
        if len(config['form_vars']) == 0:
            msg:str = "Se ha detectado un problema con el proyecto actual. Por favor, póngase en contacto con EONIA "
            flash(msg, 'error')
        return config

    async def __set_db__() -> DataBase:
        """se encarga de construir la base de datos, la tabla y columnas
        """
        db: DataBase = DataBase(config['db_file'])
        _col_names: list = [var['label'] for var in config['form_vars']]
        db.build_table(column_names=_col_names,
                       version=config['version'])
        return db

    _project_path: str = os.path.join(PROJECTS_DIR, project)
    _conf_path: str = os.path.join(PROJECTS_DIR, project, 'config.json')

    if not __validate_project__(_project_path, _conf_path):
        msg:str = "Se ha detectado un problema con el proyecto actual. Por favor, póngase en contacto con EONIA "
        flash(msg, 'error')
        return redirect('/')

    config: dict = __load_vars__(conf_file=_conf_path)
    db: DataBase = await __set_db__()
    form: FlaskForm = await BuildForm(config['form_vars'])

    """Validacion del formulario"""
    if form.validate_on_submit():
        form_data = form.data
        form_data.pop('csrf_token')
        guardado: bool = db.add(form_data)
        if guardado:
            message: str = "La informacion se guardo correctamente."
            flash(message, 'success')
        else:
            message: str = "La informacion no se guardo correctamente."
            flash(message, 'error')
        return redirect(f'/form/{project}')

    return render_template(template, form=form, project=project)
