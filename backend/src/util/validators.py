import json
import logging

validators = {}
def getValidator(collection_name: str):
    """Obtain a validator object of a collection which is stored as a json file with the same name. The validator must comply to a schema validation format (see https://www.mongodb.com/docs/manual/core/schema-validation/)

    parameters:
        collection_name -- the name of the collection, which should also be the filename

    returns:
        validator -- dict in the format of a MongoDB collection validator
    """
    if collection_name not in validators:
        logging.debug(f"Loading validator for collection: {collection_name}")
        with open(f'./src/static/validators/{collection_name}.json', 'r') as f:
            validators[collection_name] = json.load(f)
    else:
            logging.debug(f"Validator for collection {collection_name} already loaded.")
    return validators[collection_name]