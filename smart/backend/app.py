from flask import Flask
from backend.config import Config
from backend.database.db import db
from backend.routes.auth import auth_bp
from backend.routes.books import books_bp
from backend.routes.prediction import prediction_bp
from backend.routes.notifications import notifications_bp
from backend.routes.students import students_bp



def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(students_bp)

    with app.app_context():
        db.create_all()

    return app
