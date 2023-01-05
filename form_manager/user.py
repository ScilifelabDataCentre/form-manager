"""Endpoints related to auth."""

import flask

from . import csrf, oauth

blueprint = flask.Blueprint("user", __name__)  # pylint: disable=invalid-name


@blueprint.route("/me")
def user_info():
    """Perform a login using OpenID Connect."""
    return flask.jsonify({"user": flask.session.get("email", "")})


@csrf.exempt
@blueprint.route("/login")
def oidc_login():
    """Perform a login using OpenID Connect."""
    redirect_uri = flask.url_for("user.oidc_authorize", _external=True)
    return oauth.oidc_entry.authorize_redirect(redirect_uri)


@csrf.exempt
@csrf.set_cookie
@blueprint.route("/login/authorize")
def oidc_authorize():
    """Authorize a login using OpenID Connect (e.g. Elixir AAI)."""
    token = oauth.oidc_entry.authorize_access_token()
    domain_limit = flask.current_app.config["USER_FILTER"].get("email")
    if domain_limit:
        user_email = token.get("userinfo", {}).get("email")
        try:
            domain = user_email[user_email.index("@") + 1 :]
        except ValueError:
            flask.abort(400)
        if domain not in domain_limit:
            flask.abort(403)

    flask.session["email"] = token.get("userinfo", {}).get("email")
    flask.session.permanent = True

    return flask.redirect("/")


@blueprint.route("/logout")
def logout():
    """Log out a user by clearing the session cookie."""
    flask.session.clear()
    flask.session.permanent = False
    return flask.redirect("/")
