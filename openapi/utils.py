import json


def model_to_dict(model):
    return json.loads(model.json().replace('in_', 'in').replace('schema_', 'schema').replace('not_', 'not'))