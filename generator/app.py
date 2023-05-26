import pathlib

import config

from fastapi import FastAPI

from generator import dynamic
from openapi import loaders, resolvers, utils

# Główna instancja API, do której dodawane są endpoint-y
api = FastAPI()

# Ładowanie dokumentacji
doc_path = pathlib.Path(config.MAIN_DIR, 'openapi.json')
document = loaders.load_document(doc_path)

for path, path_object in document.paths.items():

    methods = resolvers.resolve_methods(path_object)

    for method, method_object in methods.items():

        endpoint = dynamic.generate_endpoint(method_object)

        # Konwertuje wszystkie możliwe odpowiedzi do typu dict
        responses = {response: method_object.responses.get(response).dict() for response in method_object.responses}

        # Dodaje ścieżkę do API
        api.add_api_route(
            path=path,
            endpoint=endpoint,
            methods=[method],
            description=method_object.description,
            operation_id=method_object.operationId,
            responses=responses,
            openapi_extra=utils.model_to_dict(method_object),
        )
