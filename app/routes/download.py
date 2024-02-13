import os
from flask import (send_file, redirect, flash)
from . import (routes_bp)


@routes_bp.route('/get/<project>', methods=['GET'])
async def download(project: str):
    dbfile: str = os.path.join('projects', project, 'db.sqlite')
    # return dbfile
    try:
        return send_file(dbfile, as_attachment=True)
    except FileNotFoundError:
        flash('Archivo no encontrado, intente mas tarde', 'error')
        return redirect('/')
