from flask import (redirect, flash)
from . import routes_bp


@routes_bp.app_errorhandler(Exception)
def handle_error(error):
    """Vista para manejo de errores
    """
    flash(error.description, 'error')
    return redirect('/')
