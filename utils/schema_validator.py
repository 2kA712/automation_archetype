import json

import jsonschema.exceptions
from jsonschema import validate


def validate_json_schema(json_obj, schema_name):
    """This function will validate json_obj's schema by comparing static/valid schema
    If obj and schema is not matched validate will throw ValidationError
    :param json_obj: json object will be reviewed
    :param schema_name: name of static schema file
    :return: bool
    """

    schema_location = f'./data/schema/{schema_name}.json'
    with open(schema_location, "r") as file:
        content = json.loads(file.read())
    try:
        validate(json_obj, content)
    except jsonschema.exceptions.ValidationError:
        return False
    return True
