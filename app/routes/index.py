import os
from glob import glob
from flask import (render_template)

from . import (routes_bp, PROJECTS_DIR)


async def __get_active__projects() -> list:
    """Busca los proyectos en la carpteta designada"""
    data: list = []
    projects_dir: str = os.path.join(PROJECTS_DIR, '*',
                                     'config.json')
    for project in glob(projects_dir):
        project_folder, _ = os.path.split(project)
        _, project_name = os.path.split(project_folder)
        data.append(project_name)
    
    return data


@routes_bp.route('/', methods=['GET'])
async def index():
    """Vista principal del proyecto
    """
    template:str = 'index.html'
    data:dict = {
        'active_projects': []
    }
    title:str = 'Inicio'
    
    data['active_projects'].extend(await __get_active__projects())
    
    return render_template(template, data=data, title=title)
