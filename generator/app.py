from fastapi import FastAPI

from generator import dynamic
from openapi import loaders, resolvers, utils

# The main API instance to which endpoints are added
api = FastAPI()

# Documentation loading
document = loaders.load_document()

# For each method (get, post etc.) for each path generates route with endpoint and adds it to the API
for path, path_object in document.paths.items():

    methods = resolvers.resolve_methods(path_object)

    for method, method_object in methods.items():

        endpoint = dynamic.generate_endpoint(method_object)

        # Converts all possible answers to dict type
        responses = {response: method_object.responses.get(response).dict() for response in method_object.responses}

        # Adds a path to the API
        api.add_api_route(
            path=path,
            endpoint=endpoint,
            methods=[method],
            description=method_object.description,
            operation_id=method_object.operationId,
            responses=responses,
            openapi_extra=utils.model_to_dict(method_object),
        )
