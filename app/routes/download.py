import csv
from io import StringIO
from flask import (Response, redirect, flash)
from app import db
from . import (routes_bp)


@routes_bp.route('/get/<project>/<version>', methods=['GET'])
async def download(project: str, version: str):
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
