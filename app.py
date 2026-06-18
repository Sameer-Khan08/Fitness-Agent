"""
app.py
------
Main entry point for the TrainWise AI Flask application.

Run with:
    python app.py
    flask --app app run --debug
"""

from flask import Flask

from src.config.settings import APP_ENV, FLASK_SECRET_KEY
from src.web.routes import web_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder="src/web/templates",
        static_folder="src/web/static",
    )
    app.secret_key = FLASK_SECRET_KEY
    app.register_blueprint(web_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=APP_ENV == "development")
