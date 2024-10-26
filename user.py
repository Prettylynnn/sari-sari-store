from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def check_password(self, password):
        """Check the hashed password against the provided password."""
        return check_password_hash(self.password, password)

    def get_id(self):
        """Return the user ID for Flask-Login."""
        return str(self.user_id)

    @property
    def is_active(self):
        """Return True, as all users are active by default."""
        return True

    @property
    def is_authenticated(self):
        """Return True, as the user is authenticated if they are logged in."""
        return True

    @property
    def is_anonymous(self):
        """Return False, as this is not an anonymous user."""
        return False
