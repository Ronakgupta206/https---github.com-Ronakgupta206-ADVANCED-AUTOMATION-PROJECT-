from backend.app import create_app
from backend.services.scheduler import start_scheduler
from backend.database.db import db

app = create_app()
start_scheduler()

if __name__ == '__main__':
    app.run(debug=True)