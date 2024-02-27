import csv
from io import StringIO
from flask import (Response, redirect, flash)
from app import db
from app.utils import validate_token
from . import (routes_bp)


@routes_bp.route('/get/<project>/<version>', methods=['GET', 'POST'])
async def download(project: str, version: str):

    if not validate_token(project_name=project):
        return redirect('/')

    collection_name: str = "{}-{}".format(project, version)
    data = db.get(collection_name)
    if len(data):
        csv_output = StringIO()
        headers = data[0].keys() if data else []
        writer = csv.DictWriter(csv_output, fieldnames=headers)
        writer.writeheader()
        for doc in data:
            writer.writerow(doc)
        csv_output.seek(0)
        return Response(
                csv_output,
                mimetype="text/csv",
                headers={"Content-disposition":f"attachment; filename={project}-{version}.csv"}
        )

    flash('El proyecto aun no tiene datos! intente mas tarde', 'error')
    return redirect('/')
