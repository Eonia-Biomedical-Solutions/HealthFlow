import os
from flask import Blueprint

routes_bp:Blueprint = Blueprint(name='public',
                                import_name=__name__,
                                )

PROJECTS_DIR:str = os.path.join('app', 'projects')

from . import index
from . import form
from . import error
from .download import download

__all__:list = ['index', 'form', 'error', 'download', 'routes_bp']
