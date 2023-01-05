"""Implementation of DataSource using MongoDB as data backend."""

from bson import ObjectId
import pymongo

from form_manager import data_source as ds


class MongoDatabase(ds.DataSource):
    """MongoDB implementation of the DataSource interface."""

    def __init__(self, config):
        """
        Set up a connection to the database.

        Args:
            config (dict): The required configuration settings.
        """
        self._client = pymongo.MongoClient(
            host=config.get("host"),
            port=config.get("port"),
            username=config.get("username"),
            password=config.get("password"),
        )
        self._db = self._client.get_database(config.get("database"))

    def fetch_forms(self, user_email):
        """
        Fetch all forms owned by the provided user.

        Args:
            user_email (str): The email of the user.

        Returns:
            list: The fetched forms.
        """
        return list(self._db["forms"].find({"owners": user_email}, {"_id": 0}))

    def fetch_form(self, identifier):
        """
        Fetch the information of the ``identifier`` form.

        Args:
            identifier (str): the form identifier.
        """
        return self._db["forms"].find_one({"identifier": identifier}, {"_id": 0})

    def add_form(self, entry):
        """
        Add a form with the provided content.

        Args:
            entry (dict): The form information.

        Returns:
            bool: Whether the form was added successfully.
        """
        return bool(self._db["forms"].insert_one(entry).inserted_id)

    def edit_form(self, entry):
        """
        Edit the form with the provided content.

        The edit should be adding/updating, not replacing
        (do not remove keys that are missing in ``entry``).

        Args:
            entry (dict): The form content. Must include the identifier.

        Returns:
            bool: Whether the form was changed successfully.
        """
        return bool(
            self._db["forms"]
            .update_one({"identifier": entry["identifier"]}, {"$set": entry})
            .matched_count
        )

    def delete_form(self, identifier):
        """
        Delete the ``identifier`` form and any related submissions.

        Args:
            identifier (dict): The form identifier.

        Returns:
            bool: Whether the form was deleted successfully.
        """
        res1 = self._db["forms"].delete_one({"identifier": identifier})
        self._db["submissions"].delete_many({"identifier": identifier})
        return bool(res1.deleted_count)

    def fetch_submissions(self, form_identifier):
        """
        Fetch all submissions belonging to the provided form.

        Args:
            form_identifier (str): The identifier for the form.

        Returns:
            list: The fetched submissions.
        """
        return list(self._db["submissions"].find({"identifier": form_identifier}))

    def add_submission(self, data):
        """
        Add a submission to a form with the provided content.

        Args:
            data (dict): The submission content.

        Returns:
            bool: Whether the submission was added successfully.
        """
        return bool(self._db["submissions"].insert_one(data).inserted_id)

    def delete_submission(self, identifier):
        """
        Delete a submission.

        Args:
            identifier (str): The submission identifier.

        Returns:
            bool: Whether the submission was deleted successfully.
        """
        return bool(self._db["submissions"].delete_one({"_id": ObjectId(identifier)}).deleted_count)

    def close(self):
        """Close the database connection."""
        self._client.close()
