"""
session_interface.py
--------------------
Custom Flask session interface using in-memory session dictionary to bypass cookie size limits.
"""

import uuid
from flask.sessions import SessionInterface, SessionMixin


class MemorySession(dict, SessionMixin):
    """Memory-based session dictionary implementation."""
    pass


class MemorySessionInterface(SessionInterface):
    """Custom Flask SessionInterface storing data in server memory and matching with a client session UUID."""
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
