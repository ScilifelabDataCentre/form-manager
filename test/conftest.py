"""Test setup."""
import copy

import pytest

from form_manager import create_app
import test as helpers


@pytest.fixture(scope="function")
def client():
    app = create_app(testing=True)
    yield app.test_client()


FORM = {
    "identifier": "testFormTestForm",
    "title": "Test Form",
    "recaptcha_secret": "",
    "email_recipients": ["test@example.com"],
    "email_custom": True,
    "email_title": "Email from Test Form",
    "email_html_template": "<p>{{ key }}</p>",
    "email_text_template": "{{ key }}",
    "owners": ["test@example.com"],
    "redirect": "https://www.example.com",
    "blacklist": [{"blKey": "[0-9]"}],
}


@pytest.fixture(scope="function")
def form_default():
    helpers.data_source.add_form(FORM)
    yield FORM["identifier"]
    helpers.data_source.delete_form(FORM["identifier"])


@pytest.fixture(scope="function")
def form_bad_bl():
    entry = copy.deepcopy(FORM)
    entry["identifier"] = "testFormBadBList"
    entry["blacklist"] = [{"blKey": "(?)"}]

    helpers.data_source.add_form(entry)
    yield entry["identifier"]
    helpers.data_source.delete_form(entry["identifier"])
