import typing

import consts


class Dynamic(object):
    """
    WARNING
    This class is fucking alive :D
    """

    @classmethod
    def add(cls, **kwargs):
        raise Exception('Method defined only for override')

class DynamicResponseModels(Dynamic):

    @classmethod
    def _get_type(cls, schema_object: dict):
        """
        Returns (even nested) types of provided OA property
        :param schema_object: OA schema object
        :return: Type
        """
        # get schema "type" string
        schema_type = schema_object.get('type')

        # get python type by OA type
        py_type_obj = consts.TYPES.get(schema_type)
        if not py_type_obj:
            raise RuntimeError(f'Unknown type: {schema_type}')

        # get python type from const
        py_type = py_type_obj.get('type')
        # check nested attribute
        if not py_type_obj.get('nested'):
            return py_type

        if py_type == object:
            # get schema "properties" object
            schema_properties = schema_object.get('properties')

            properties_types = {}
            for prop in schema_properties:
                properties_types[prop] = cls._get_type(schema_properties.get(prop))
            return typing.Dict[str, typing.TypedDict('Property', properties_types)]

        elif py_type == list:
            # get schema "items" object
            schema_items = schema_object.get('items')
            return typing.List[cls._get_type(schema_items)]

    @classmethod
    def add(cls, name, schema_object: dict):
        # get schema "type" string
        schema_type = schema_object.get('type')
        # get schema "properties" object
        schema_properties = schema_object.get('properties')
        if schema_type != 'object':
            raise RuntimeError(f'Response models refers to "object" type, not "{schema_type}"')
        model_properties = {}
        for schema_property in schema_properties:
            model_properties[schema_property] = cls._get_type(schema_properties.get(schema_property))
        dynamic_response_model = type(name, (object,), model_properties)
        setattr(cls, name, dynamic_response_model)
        return getattr(cls, name)

class DynamicPathOperations(Dynamic):


    @classmethod
    def add(cls, path: str, method: str, operation_object: dict):

        # operation_example = {
        #     "description": "Returns all pets from the system that the user has access to",
        #     "responses": {
        #         "200": {
        #             "description": "A list of pets.",
        #             "content": {
        #                 "application/json": {
        #                     "schema": {
        #                         "type": "array",
        #                         "items": {
        #                             "$ref": "#/components/schemas/pet"
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }
        decorator = consts.METHODS.get(method)

        description: str = operation_object.get('description')
        responses: dict = operation_object.get('responses')

        for response in responses:
            status: str = response
            response_obj: dict = responses.get(response)
            response_description: str = response_obj.get('description')
            response_content: dict = response_obj.get('content')

            for response_format in response_content:
                format_obj: dict = response_content.get(response_format)
                response_schema: dict = format_obj.get('schema')
                schema_type: str = response_schema.get('type')

                endpoint_schema = {
                    'path': path
                }

                if schema_type == 'object':
                    response_model = DynamicResponseModels.add()

                @decorator(**endpoint_schema)
                def path_operation():
                    response = {'dupa': 'dziala'}
                    print(f'Created {method.upper()} {path}')
                    return response

                path_operation.__doc__ = f'Dynamically created path operation {description}'
                name = f'{path[1:].replace("/", "_")}'
                path_operation.__name__ = name
                setattr(cls, path_operation.__name__, path_operation)
                return getattr(cls, name)
