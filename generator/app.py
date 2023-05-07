import json
import pathlib

import config

from fastapi import FastAPI, Request

from loggers import main_logger
from openapi import loaders, resolvers

# Główna instancja API, do której dodawane są endpoint-y
api = FastAPI()

# Ładowanie dokumentu
doc_path = pathlib.Path(config.MAIN_DIR, 'openapi.json')
document = loaders.load_document(doc_path)

paths = document.paths


def endpoint(request: Request):
    """
    Uniwersalna metoda endpoint-a, która wyszukuje wołaną ścieżkę i generuje odpowiedź złożoną z losowych danych
    :param request: wbudowany parametr
    :return:
    """

    url = request.url.path

    main_logger.debug(url)

    return resolvers.resolve_path(paths, url)


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
