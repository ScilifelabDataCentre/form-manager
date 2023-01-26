"""Form-related tests."""

import test as helpers


def test_list_forms_anon(client):
    """
    1. as anon, list forms (fail)
    """
    response = client.get("/api/v1/form")
    assert response.status_code == 403


def test_list_forms_user(client):
    """
    1. as user, list forms (ok)
    """
    helpers.login(helpers.USERS[0], client)
    response = client.get("/api/v1/form")
    assert response.status_code == 200
    assert response.json == {"forms": [], "url": "http://localhost/api/v1/form"}


def test_add_form_anon(client):
    """
    1. as anon, add form (fail)
    """
    response = client.post("/api/v1/form")
    assert response.status_code == 403


def test_add_list_delete_form(client):
    """
    1. as user, create form (ok)
    2. as user, list form (ok)
    5. as user, delete form (ok)
    """
    helpers.login(helpers.USERS[0], client)

    response = client.post("/api/v1/form")
    assert response.status_code == 200
    identifier = response.json["identifier"]
    assert helpers.data_source.fetch_form(identifier)

    response = client.get(f"/api/v1/form/{identifier}")
    assert response.status_code == 200
    assert "form" in response.json

    response = client.delete(f"/api/v1/form/{identifier}")
    assert response.status_code == 200
    assert not helpers.data_source.fetch_form(identifier)


def test_add_list_delete_form_not_allowed(client):
    """
    1. as user, create form (ok)
    2. as anon, list form (fail)
    2. as anon, delete form (fail)
    3. as other user, list form (fail)
    4. as other user, delete form (fail)
    5. as user, delete form (ok)
    """
    helpers.login(helpers.USERS[0], client)
    response = client.post("/api/v1/form")
    assert response.status_code == 200
    identifier = response.json["identifier"]

    helpers.logout(client)
    response = client.get(f"/api/v1/form/{identifier}")
    assert response.status_code == 403
    response = client.delete(f"/api/v1/form/{identifier}")
    assert response.status_code == 403

    helpers.login(helpers.USERS[1], client)
    response = client.get(f"/api/v1/form/{identifier}")
    assert response.status_code == 403
    response = client.delete(f"/api/v1/form/{identifier}")
    assert response.status_code == 403

    helpers.login(helpers.USERS[0], client)
    response = client.delete(f"/api/v1/form/{identifier}")
    assert response.status_code == 200


def test_receive_submission_blacklist_accept(client, form_default):
    """
    1. Submit a form
    2. Verify that it is accepted by the blacklist
    """
    data = {"blKey": "abc"}
    response = client.post(f"/api/v1/form/{form_default}/incoming", data=data)
    assert response.status_code == 302
    assert response.location == "/success?redirect=https://www.example.com"
    assert helpers.data_source.fetch_submissions(form_default)


def test_receive_submission_blacklist_reject(client, form_default):
    """
    1. Submit a form
    2. Verify that it is rejected by the blacklist
    """
    data = {"blKey": "123"}
    response = client.post(f"/api/v1/form/{form_default}/incoming", data=data)
    assert response.status_code == 302
    assert response.location == "/success?redirect=https://www.example.com"
    assert not helpers.data_source.fetch_submissions(form_default)


def test_receive_submission_blacklist_bad_regex_accept(client, form_bad_bl):
    """
    1. Submit a form
    2. Verify that it is accepted by the blacklist
    """
    data = {"blKey": "123"}
    response = client.post(f"/api/v1/form/{form_bad_bl}/incoming", data=data)
    assert response.status_code == 302
    assert response.location == "/success?redirect=https://www.example.com"
    assert helpers.data_source.fetch_submissions(form_bad_bl)
