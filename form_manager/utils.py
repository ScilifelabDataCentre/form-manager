"""General helper functions."""
from datetime import datetime
import functools
import json
import os
import secrets

import flask
import flask_mail
import jinja2
from jinja2.exceptions import TemplateSyntaxError
import pytz
import requests


def make_timestamp():
    """
    Generate a timestamp of the current time.

    returns:
        datetime: The current time.
    """
    fmt = "%a, %d %b %Y %H:%M:%S %Z"
    return datetime.now(pytz.timezone(os.environ.get("TZ", "Europe/Stockholm"))).strftime(fmt)


def verify_recaptcha(secret: str, response: str):
    """
    Verify the secret from a recaptcha.

    Args:
        secret (str): The secret value for the recaptcha
        response (str): The response value from the form (g-recaptcha-response)

    Returns:
        bool: Whether the check passed
    """
    rec_check = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        {"secret": secret, "response": response},
        timeout=5,
    )
    return bool(rec_check.json().get("success"))


def login_required(func):
    """Check whether user is logged in, otherwise return 403."""

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not flask.session.get("email"):
            flask.abort(code=403)
        return func(*args, **kwargs)

    return inner


def generate_id():
    """Generate an identifier for a form entry."""
    return secrets.token_urlsafe(12)


def has_form_access(username, entry):
    """
    Verify that the given user may access a specific entry.

    Args:
        username (str): The username (e.g. email) of the user.
        entry (dict): The form entry.

    Returns:
        bool: Whether the user has access.
    """
    if not username:  # in case there is somehow an empty string in owners
        return False
    return username in entry["owners"]


def apply_template(template: str, data: dict) -> str:
    """
    Fill a jinja style template with the values of the defined variables.

    Args:
        template (str): The template.
        data (dict): The variables to use.

    Raises:
        ValueError: The template application failed.

    Returns:
        str: The resulting text.
    """
    try:
        jinja_env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=jinja2.select_autoescape(
                default_for_string=True,
                default=True,
            ),
        ).from_string(template)
    except TemplateSyntaxError as exc:
        raise ValueError("Unable to use the template in Jinja") from exc
    return jinja_env.render(**data)


def gen_json_body(data: dict) -> str:
    """
    Generate a email body with formatted JSON.

    Args:
        data (dict): The data to include.

    Returns:
        str: The generated body text.
    """
    body = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    body += f"\n\nSubmission received: {make_timestamp()}"
    return body


def send_email(form_info: dict, data: dict, mail_client):
    """
    Send an email with the submitted form content.

    Args:
        form_info (dict): Information about the form.
        data (dict): The submitted form.
    """
    if form_info.get("email_custom"):
        try:
            body_text = apply_template(form_info.get("email_text_template", ""), data)
            body_html = apply_template(form_info.get("email_html_template", ""), data)
        except ValueError:
            body_text = (
                "There are error(s) in the email template(s), using the default JSON format\n\n"
            )
            body_text += gen_json_body(data)
            body_html = body_text.replace("\n", "<br/>")
    else:
        body_text = gen_json_body(data)
        body_html = body_text.replace("\n", "<br/>")
    mail_client.send(
        flask_mail.Message(
            form_info.get("email_title"),
            body=body_text,
            html=body_html,
            recipients=form_info["email_recipients"],
        )
    )
