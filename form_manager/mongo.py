"""Implementation of DataWrapper using MongoDB as data backend."""

import pymongo

from form_manager import data_wrapper as dw


class MongoDatabase(dw.DataWrapper):
    def __init__(self, config):
        self._client = pymongo.MongoClient(
            host=config.get("host"),
            port=config.get("port"),
            username=config.get("username"),
            password=config.get("password"),
        )
        self._db = self._client.get_database(config.get("database"))

    def get_forms(self, user_email):
        return list(self._db["forms"].find({"owners": user_email}, {"_id": 0}))

    def get_form(self, identifier):
        return self._db["forms"].find_one({"identifier": identifier}, {"_id": 0})

    def add_form(self, entry):
        return self._db["forms"].insert_one(entry)

    def update_form(self, entry):
        return self._db["forms"].update_one({"_id": entry["_id"]}, {"$set": entry})

    def delete_form(self, identifier):
        res1 = self._db["forms"].delete_one({"identifier": identifier})
        res2 = self._db["submissions"].delete_many({"identifier": identifier})
        return res1, res2

    def get_submissions(self, form_identifier):
        return list(flask.g.db["submissions"].find({"identifier": form_identifier}))

    def add_submission(self, data):
        return self._db["submissions"].insert_one(data)

    def delete_submission(self, identifier):
        return self._db["submissions"].delete_one({"_id": ObjectId(identifier)})

    def close(self):
        self._client.close()
