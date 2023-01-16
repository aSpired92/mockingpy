import importlib
import os.path
from pathlib import Path
from typing import List

import datamodel_code_generator as model_generator

import config

from fastapi import FastAPI
from fastapi.openapi import models


from openapi import loaders


class Dynamic:

    @classmethod
    def add_endpoint(cls, parameters: List[models.Parameter]):
        query_params = ''
        if parameters:
            for param in parameters:
                if param.in_ == models.ParameterInType.query:
                    query_params += param.name + ','
        local_dict = {}

        code = f"""
async def response_data({query_params}):
    return {{'dupa': 'aaa'}}
        """

        print(code)

        exec(code, globals(), local_dict)

        response_data = local_dict['response_data']
        setattr(cls, 'response_data', response_data)


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
            Dynamic().add_endpoint(method_object.parameters)

            responses = {response: method_object.responses.get(response).dict() for response in method_object.responses}

            params = {
                'path': path,
                'endpoint': getattr(Dynamic, 'response_data'),
                'methods': [method],
                'description': method_object.description,
                'operation_id': method_object.operationId,
                'responses': responses
            }

            api.add_api_route(**params)
