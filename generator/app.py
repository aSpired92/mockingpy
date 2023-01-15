import importlib
import os.path
from pathlib import Path
from typing import Union, List, Dict

import datamodel_code_generator as model_generator
from fastapi.openapi.models import Response

import config

from fastapi import FastAPI
from fastapi.openapi import models


from openapi import loaders


NO_DESCRIPTION = 'No description'


def get_ref_name(ref):
    return str(ref).split('/')[-1]


def get_model(ref_nam):
    return getattr(response_models, ref_nam)

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
doc_path = os.path.join(config.MAIN_DIR, 'openapi.yaml')
document = loaders.DocumentLoader.load(doc_path)

model_generator.generate(input_=Path(doc_path), input_file_type=model_generator.InputFileType.OpenAPI, output=Path(config.MODELS_DIR))

response_models = importlib.import_module('dynamic.models')

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
            # Converts responses to dicts
            if method_object.parameters:
                Dynamic().add_endpoint(method_object.parameters)

            params = {
                'path': path,
                'endpoint': getattr(Dynamic, 'response_data'),
                'methods': [method],
                'description': method_object.description,
                'operation_id': method_object.operationId

            }

            responses = {}

            for response in method_object.responses:
                response_object = method_object.responses.get(response)
                new_response = {
                    'description': response_object.description,
                }

                if response_object.content:
                    new_content = {}
                    for content in response_object.content:
                        new_content_type = {}
                        content_object = response_object.content.get(content)
                        if content_object.example:
                            new_content_type['example'] = content_object.example
                            new_content[content] = new_content_type
                        schema = content_object.schema_

                        if schema.items:
                            ref_name = get_ref_name(schema.items.ref)
                            new_response['model'] = List[get_model(ref_name)]
                        elif schema.ref:
                            new_response['model'] = get_model(get_ref_name(schema.ref))

                    new_response['content'] = new_content

                responses[response] = new_response

            params['responses'] = responses

            api.add_api_route(**params)