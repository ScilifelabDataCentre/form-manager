"""Helper functions for tests."""

from form_manager import config, data


def login(email, client):
    return client.get(f"/api/v1/development/login/{email}")


def logout(client):
    return client.get(f"/api/v1/user/logout")


USERS = ["test@example.com", "test2@example.com"]

data_source = data.activate(config.Config().DB_CONF)
