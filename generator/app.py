import importlib
import json
import os.path
from pathlib import Path
from typing import List

import datamodel_code_generator as model_generator

import config

from fastapi import FastAPI
from fastapi.openapi import models


from openapi import loaders


def endpoint():
    return 'ok'

api = FastAPI()
doc_path = os.path.join(config.MAIN_DIR, 'openapi.json')
document = loaders.DocumentLoader.load(doc_path)


paths = document.paths

for path in paths:
    path_object = paths.get(path)
    methods = {
        'get': path_object.get,
        'post': path_object.post,
        'put': path_object.put,
        'delete': path_object.delete,
        'options': path_object.options,
        'head': path_object.head,
        'patch': path_object.patch,
        'trace': path_object.trace
    }

    for method in methods:
        method_object = methods.get(method)
        if method_object:

            responses = {response: method_object.responses.get(response).dict() for response in method_object.responses}

            params = {
                'path': path,
                'endpoint': endpoint,
                'methods': [method],
                'description': method_object.description,
                'operation_id': method_object.operationId,
                'responses': responses,
                'openapi_extra': json.loads(method_object.json().replace('in_', 'in').replace('schema_', 'schema').replace('not_', 'not'))
            }

            print(json.loads(method_object.json().replace('in_', 'in').replace('schema_', 'schema').replace('not_', 'not')))

            api.add_api_route(**params)
