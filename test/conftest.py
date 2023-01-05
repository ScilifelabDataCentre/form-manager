"""Test setup."""

import pytest

from form_manager import create_app


@pytest.fixture(scope="function")
def client():
    app = create_app(testing=True)
    yield app.test_client()
