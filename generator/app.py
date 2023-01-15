import importlib
import os.path
from pathlib import Path
from typing import Union, List

import datamodel_code_generator as model_generator
from fastapi.openapi.models import Response

import config

from fastapi import FastAPI

from openapi import loaders


NO_DESCRIPTION = 'No description'

def get_ref_name(ref):
    return str(ref).split('/')[-1]


def get_model(ref_nam):
    return getattr(response_models, ref_nam)

async def response_data():
    return Response(None)


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

            params = {
                'path': path,
                'endpoint': response_data,
                'methods': [method],
                'description': method_object.description
            }

            responses = {}

            for response in method_object.responses:
                response_object = method_object.responses.get(response)
                new_response = {
                    'description': response_object.description
                }

                if response_object.content:
                    for content in response_object.content:
                        content_object = response_object.content.get(content)
                        schema = content_object.schema_

                        if schema.items:
                            ref_name = get_ref_name(schema.items.ref)
                            new_response['model'] = List[get_model(ref_name)]
                        elif schema.ref:
                            new_response['model'] = get_model(get_ref_name(schema.ref))

                responses[response] = new_response

            params['responses'] = responses

            api.add_api_route(**params)