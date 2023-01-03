"""Config for DDS setup."""
import os


class Config:
    """Base config"""

    SITE_NAME = "Form Manager"
    SECRET_KEY = "REPLACE_THE_STRING_IN_PRODUCTION"

    SESSION_COOKIE_SECURE = False  # Should be True for any setup with support for https

    DB_CONF = {
        "host": "db",
        "port": 27017,
        "username": "mongoadmin",
        "password": "mongopassword",
        "database": "FormManager",
    }

    OIDC_ID = ""
    OIDC_SECRET = ""
    OIDC_METADATA = ""

    MAIL_SERVER = "mailcatcher"
    MAIL_PORT = 1025
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = ("Form Manager", "forms@example.com")

    USER_FILTER = {}  # Limits to users that may use the system, e.g. {"email": ["scilifelab.se"]}

    REVERSE_PROXY = False  # Behind a reverse proxy, use X_Forwarded-For to get the ip
