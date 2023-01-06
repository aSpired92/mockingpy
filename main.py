import os.path

import yaml
import dynamic
import config


def get_document():
    with open(os.path.join(config.MAIN_DIR, 'openapi.yaml')) as f:
        data: dict = yaml.load(f, Loader=yaml.SafeLoader)
        return data


def prepare_models():
    document: dict = get_document()
    components: dict = document.get('components')
    schemas: dict = components.get('schemas')

    for schema in schemas:
        name = schema
        print(f'Name: {name}')
        schema_object: dict = schemas.get(schema)
        print(f'Type: {schema_object.get("type")}')
        response_model = dynamic.DynamicResponseModels.add(name, schema_object)
        print(f'Response model {name}: {response_model.__dict__}')



if __name__ == '__main__':
    prepare_models()

