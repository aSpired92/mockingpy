import json
import pathlib

import config

from fastapi import FastAPI, Request
from openapi import loaders, resolvers

api = FastAPI()

doc_path = pathlib.Path(config.MAIN_DIR, 'openapi.json')
document = loaders.DocumentLoader.load(doc_path)

paths = document.paths


def endpoint(request: Request):

    url = request.url.path

    if request.path_params:
        filtered_paths = {key: paths.get(key) for key in paths if paths.get(key).dict().get(request.method.lower())}
        path_object = resolvers.resolve_path(filtered_paths, url)
    else:
        path_object = paths.get(url)

    return path_object


def generate_paths():
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

                api.add_api_route(**params)


generate_paths()
