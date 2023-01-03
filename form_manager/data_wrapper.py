"""Abstraction of the data backend."""

from form_manager import mongo


class DataWrapper:
    """Abstract interface for the data backend."""

    def __init__(self, config):
        raise NotImplementedError

    def get_forms(self, user):
        raise NotImplementedError

    def get_form(self, identifier):
        raise NotImplementedError

    def add_form(self, entry):
        raise NotImplementedError

    def update_form(self, entry):
        raise NotImplementedError

    def delete_form(self, identifier):
        raise NotImplementedError

    def get_submissions(self, form_identifier):
        raise NotImplementedError

    def add_submission(self, data):
        raise NotImplementedError

    def delete_submission(self, identifier):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
