"""
app.py
------
Main entry point for the TrainWise AI Flask application.

Run with:
    python app.py
    flask --app app run --debug
"""

import uuid
from flask import Flask
from flask.sessions import SessionInterface, SessionMixin

from src.config.settings import APP_ENV, FLASK_SECRET_KEY
from src.web.routes import web_bp


class MemorySession(dict, SessionMixin):
    pass


class MemorySessionInterface(SessionInterface):
    def __init__(self):
        self.store = {}

    def open_session(self, app, request):
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        sid = request.cookies.get(cookie_name)
        if not sid or sid not in self.store:
            sid = str(uuid.uuid4())
            self.store[sid] = MemorySession()
        self.store[sid]["_sid"] = sid
        return self.store[sid]

    def save_session(self, app, session, response):
        sid = session.get("_sid")
        if not sid:
            return
        
        self.store[sid] = session
        
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        expires = self.get_expiration_time(app, session)
        
        cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        response.set_cookie(
            cookie_name,
            sid,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite,
        )


def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder="src/web/templates",
        static_folder="src/web/static",
    )
    app.secret_key = FLASK_SECRET_KEY
    app.session_interface = MemorySessionInterface()
    app.register_blueprint(web_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=APP_ENV == "development")
