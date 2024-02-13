import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    project_folder: str = os.path.join('app', 'projects')
    os.makedirs(project_folder, exist_ok=True)
    app.run(debug=False)
