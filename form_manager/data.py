"""Load and activate the data backend."""

from form_manager import mongo


def activate(config: dict):
    """Activate the chosen data source."""
    data_source_name = "mongodb"
    data_source = None
    if data_source_name == "mongodb":
        data_source = mongo.MongoDatabase(config)
    return data_source
