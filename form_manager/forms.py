"""Endpoints related to forms."""
import flask

from . import csrf, mail, utils

blueprint = flask.Blueprint("forms", __name__)  # pylint: disable=invalid-name


def form():
    """The data structure for a form"""
    return {
        "identifier": utils.generate_id(),
        "title": "",
        "recaptcha_secret": "",
        "email_recipients": [],
        "email_custom": False,
        "email_title": "",
        "email_html_template": "",
        "email_text_template": "",
        "owners": [],
        "redirect": "",
    }


def validate_form(indata: dict, reference: dict) -> bool:
    """
    Validate that the incoming data matches the form data structure.

    * No extra properties
    * All indata is of the correct type
    * Identifier is not modified

    Args:
        indata (dict): The data to be validated.
        reference (dict): The data structure to use as reference (entry or form()).

    Returns:
        bool: Whether the validation passed or not.
    """
    for prop in indata:
        if prop not in reference:
            flask.current_app.logger.debug("Extra property")
            return False
        if not isinstance(indata[prop], type(reference[prop])):
            flask.current_app.logger.debug("Wrong property type")
            return False
    if "identifier" in indata:
        if indata["identifier"] != reference["identifier"]:
            flask.current_app.logger.debug("Trying to modifify the identifier")
            return False
    if "owners" in indata:
        if flask.session.get("email") not in indata["owners"]:
            return False
    for list_prop in ("owners", "email_recipients"):
        if list_prop in indata:
            for entry in indata[list_prop]:
                if not isinstance(entry, str):
                    return False
    return True


@blueprint.route("", methods=["GET"])
@utils.login_required
def list_forms():
    """List all forms belonging to the current user."""
    form_info = flask.g.data.fetch_forms(flask.session["email"])
    return flask.jsonify(
        {"forms": form_info, "url": flask.url_for("forms.list_forms", _external=True)}
    )


@blueprint.route("/<identifier>", methods=["GET"])
@utils.login_required
def fetch_form_info(identifier: str):
    """
    Get information about a form.

    Args:
        identifier (str): The form identifier.
    """
    entry = flask.g.data.fetch_form(identifier)
    if not entry:
        flask.abort(code=404)
    if not utils.has_form_access(flask.session["email"], entry):
        flask.abort(code=403)
    return flask.jsonify(
        {
            "form": entry,
            "url": flask.url_for("forms.fetch_form_info", identifier=identifier, _external=True),
        }
    )


@blueprint.route("", methods=["POST"])
@utils.login_required
def add_form():
    """Add a new form for the current user."""
    indata = flask.request.get_json(silent=True)
    if not indata:
        indata = {}
    entry = form()
    while flask.g.data.fetch_form(entry.get("identifier")):
        entry["identifier"] = utils.generate_id()
    if not validate_form(indata, entry):
        flask.current_app.logger.debug("Validation failed")
        flask.abort(code=400)
    entry.update(indata)
    entry["owners"] = [flask.session["email"]]
    if not flask.g.data.add_form(entry):
        flask.abort(500, {"message": "Failed to add form"})
    return flask.jsonify(
        {"identifier": entry["identifier"], "url": flask.url_for("forms.add_form", _external=True)}
    )


@blueprint.route("/<identifier>", methods=["PATCH"])
@utils.login_required
def edit_form(identifier: str):
    """
    Edit a form for the current user.

    Args:
        identifier (str): The form identifier.
    """
    indata = flask.request.get_json(silent=True)
    if not indata:
        flask.abort(code=400)
    entry = flask.g.data.fetch_form(identifier)
    if not entry:
        flask.abort(code=404)
    if not utils.has_form_access(flask.session["email"], entry):
        flask.abort(code=403)
    if not validate_form(indata, entry):
        flask.current_app.logger.debug("Validation failed")
        flask.abort(code=400)
    entry.update(indata)
    if not flask.g.data.edit_form(entry):
        flask.abort(500, {"message": "Failed to edit form"})
    return flask.jsonify(
        {
            "status": "success",
            "identifier": identifier,
            "type": "PATCH",
            "url": flask.url_for("forms.edit_form", identifier=identifier, _external=True),
        }
    )


@blueprint.route("/<identifier>", methods=["DELETE"])
@utils.login_required
def delete_form(identifier: str):
    """
    Delete a form for the current user.

    Args:
        identifier (str): The form identifier.
    """
    entry = flask.g.data.fetch_form(identifier)
    if not entry:
        flask.abort(code=404)
    if not utils.has_form_access(flask.session["email"], entry):
        flask.abort(code=403)
    if not flask.g.data.delete_form(identifier):
        flask.abort(500, {"message": "Failed to delete form"})
    return ""


@csrf.exempt
@blueprint.route("/<identifier>/incoming", methods=["POST"])
def receive_submission(identifier: str):
    """
    Save a form submission to the data backend.

    Args:
        identifier (str): The form identifier.
    """
    form_info = flask.g.data.fetch_form(identifier)
    if not form_info:
        return flask.abort(code=400)
    form_submission = dict(flask.request.form)

    if form_info.get("redirect"):
        redirect_args = f"?redirect={form_info['redirect']}"
    else:
        redirect_args = ""

    if form_info.get("recaptcha_secret"):
        if "g-recaptcha-response" not in form_submission or not utils.verify_recaptcha(
            form_info["recaptcha_secret"], form_submission["g-recaptcha-response"]
        ):
            return flask.redirect(f"/failure{redirect_args}")
        del form_submission["g-recaptcha-response"]

    if form_info.get("email_recipients"):
        utils.send_email(form_info, form_submission, mail)

    to_add = {
        "submission": form_submission,
        "timestamp": utils.make_timestamp(),
        "identifier": identifier,
        "origin": flask.request.environ.get("HTTP_ORIGIN", "-"),
    }

    flask.g.data.add_submission(to_add)

    return flask.redirect(f"/success{redirect_args}")


@blueprint.route("/<identifier>/url", methods=["GET"])
@utils.login_required
def fetch_form_url(identifier: str):
    """
    Get the submission url for a form.

    Args:
        identifier (str): The form identifier.
    """
    entry = flask.g.data.fetch_form(identifier)
    if not entry:
        flask.abort(code=404)
    if not utils.has_form_access(flask.session["email"], entry):
        flask.abort(code=403)
    return flask.jsonify(
        {
            "method": "POST",
            "submission_url": flask.url_for(
                "forms.receive_submission", identifier=identifier, _external=True
            ),
        }
    )


@blueprint.route("/<identifier>/submission", methods=["GET"])
@utils.login_required
def fetch_submissions(identifier):
    """
    List form submissions.

    Args:
        identifier (str): The form identifier.
    """
    form_info = flask.g.data.fetch_form(identifier)
    if not form_info:
        flask.abort(code=404)
    if not utils.has_form_access(flask.session["email"], form_info):
        flask.abort(code=403)
        submissions = flask.g.data.fetch_submissions(identifier)
    for submission in submissions:
        submission["id"] = str(submission["_id"])
        del submission["_id"]
    return flask.jsonify(
        {
            "submissions": submissions,
            "url": flask.url_for("forms.fetch_submissions", identifier=identifier, _external=True),
        }
    )


@blueprint.route("/<identifier>/submission/<subid>", methods=["DELETE"])
@utils.login_required
def delete_submission(identifier: str, subid: str):
    """
    Delete a form submission.

    Args:
        identifier (str): The form identifier.
        subid (str): The submission identifier.
    """
    form_info = flask.g.data.fetch_form(identifier)
    if not form_info:
        flask.abort(404)
    if not utils.has_form_access(flask.session["email"], form_info):
        flask.abort(403)
    if not flask.g.data.delete_submission(subid):
        flask.abort(500, {"message": "Failed to delete entry"})
    return ""
