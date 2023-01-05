"""Abstract interface for data sources."""


class DataSource:
    """
    Abstract interface for the data backend.

    Any data returned by methods should match the data structures defined in e.g. ``forms.py``.
    """

    def __init__(self, config: dict):
        """
        Initialise the data source.

        Args:
            config (dict): Any configuration settings required by the data source.
        """
        raise NotImplementedError

    def fetch_forms(self, user_email: str) -> list:
        """
        Fetch all forms owned by the provided user.

        Args:
            user_email (str): The email of the user.

        Returns:
            list: The fetched forms.
        """
        raise NotImplementedError

    def fetch_form(self, identifier: str) -> dict:
        """
        Fetch the information of the ``identifier`` form.

        Args:
            identifier (str): the form identifier.
        """
        raise NotImplementedError

    def add_form(self, entry: dict) -> bool:
        """
        Add a form with the provided content.

        Args:
            entry (dict): The form information.

        Returns:
            bool: Whether the form was added successfully.
        """
        raise NotImplementedError

    def edit_form(self, entry: dict) -> bool:
        """
        Edit the form with the provided content.

        The edit should be adding/updating, not replacing
        (do not remove keys that are missing in ``entry``).

        Args:
            entry (dict): The form content. Must include the identifier.

        Returns:
            bool: Whether the form was changed successfully.
        """
        raise NotImplementedError

    def delete_form(self, identifier: str) -> bool:
        """
        Delete the ``identifier`` form.

        Args:
            identifier (dict): The form identifier.

        Returns:
            bool: Whether the form was deleted successfully.
        """
        raise NotImplementedError

    def fetch_submissions(self, form_identifier: str) -> list:
        """
        Fetch all submissions belonging to the provided form

        Args:
            form_identifier (str): The identifier for the form.

        Returns:
            list: The fetched submissions.
        """
        raise NotImplementedError

    def add_submission(self, data: dict) -> bool:
        """
        Add a submission to a form with the provided content.

        Args:
            data (dict): The submission content.

        Returns:
            bool: Whether the submission was added successfully.
        """
        raise NotImplementedError

    def delete_submission(self, identifier: str):
        """
        Delete a submission.

        Args:
            identifier (str): The submission identifier.

        Returns:
            bool: Whether the submission was deleted successfully.
        """
        raise NotImplementedError

    def close(self):
        """Clean up the data source, e.g. close database connections."""
        raise NotImplementedError
