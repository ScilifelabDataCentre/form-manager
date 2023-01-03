"""Load and activate the data backend."""

from form_manager import mongo


def activate(config):
    data_backend = "mongodb"
    if data_backend == "mongodb":
        return mongo.MongoDatabase(config)
