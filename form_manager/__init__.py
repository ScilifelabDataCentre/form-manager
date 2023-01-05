"""Initialize Flask app."""

import logging
import os

import flask
import flask_mail
import flask_talisman
import flask_seasurf
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix

mail = flask_mail.Mail()
oauth = OAuth()
csrf = flask_seasurf.SeaSurf()
talisman = flask_talisman.Talisman()

from form_manager import config, data, forms, user, utils  # to avoid issues with circular import


def create_app(testing=False):
    """Construct the core application."""
    app = flask.Flask("form_manager")
    if testing:
        app.config["TESTING"] = True
    app.config.from_object("form_manager.config.Config")
    app.config.from_envvar("CONFIG_FILE", silent=True)

    @app.before_request
    def prepare():
        """Set up the database connection"""
        flask.g.data = data.activate(flask.current_app.config["DB_CONF"])

    @app.after_request
    def finalize(response):
        """Finalize the response and clean up."""
        # close db connection
        flask.g.data.close()
        # add some headers for protection
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        if gunicorn_logger:
            app.logger.handlers = gunicorn_logger.handlers
            app.logger.setLevel(gunicorn_logger.level)

    mail.init_app(app)
    app.extensions["mail"].debug = 0

    oauth.init_app(app)
    oauth.register(
        "oidc_entry",
        client_id=app.config.get("OIDC_ID"),
        client_secret=app.config.get("OIDC_SECRET"),
        server_metadata_url=app.config.get("OIDC_METADATA"),
        client_kwargs={"scope": "openid profile email"},
    )

    if not app.testing:
        talisman.init_app(app)
        csrf.init_app(app)

    if app.config["REVERSE_PROXY"]:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    app.register_blueprint(forms.blueprint, url_prefix="/api/v1/form")
    app.register_blueprint(user.blueprint, url_prefix="/api/v1/user")

    @app.route("/api/v1/heartbeat", methods=["GET"])
    @talisman(force_https=False)
    def heartbeat():
        return flask.Response(status=200)

    if os.environ.get("DEV_LOGIN") or app.testing:
        activate_dev(app)

    return app


def activate_dev(app):
    """
    Activate endpoints for development.

    Never activate in a production environment
    """

    @app.route("/api/v1/development/login/<email>")
    def dev_login(email: str):
        """Force login as email."""
        flask.session["email"] = email
        return f"Logged in as {email}"
