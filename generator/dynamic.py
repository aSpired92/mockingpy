# import typing
#
# import pydantic
#
# import consts
# from fastapi.openapi import models
#
# from openapi import resolvers
#
#
# class Dynamic(object):
#     """
#     WARNING
#     This class is fucking alive :D
#     """
#
#     @classmethod
#     def add(cls, **kwargs):
#         raise Exception('Method defined only for override')
#
#     @property
#     def list(self):
#         raise Exception('Method defined only for override')
#
#
# class DynamicResponseModels(Dynamic):
#
#     @classmethod
#     def _get_type(cls, schema_object: models.Schema):
#         """
#         Returns (even nested) types of provided OA property
#         :param schema_object: OA schema object
#         :return: Type
#         """
#         # get schema "type" string
#         schema_type = schema_object.type
#
#         # get python type by OA type
#         py_type_obj = consts.TYPES.get(schema_type)
#         if not py_type_obj:
#             raise RuntimeError(f'Unknown type: {schema_type}')
#
#         # get python type from const
#         py_type = py_type_obj.get('type')
#         # check nested attribute
#         if not py_type_obj.get('nested'):
#             return py_type
#
#         if py_type == object:
#             # get schema "properties" object
#             schema_properties = schema_object.properties
#
#             properties_types = {}
#             for prop in schema_properties:
#                 properties_types[prop] = cls._get_type(schema_properties.get(prop))
#             return typing.Dict[str, typing.TypedDict('Property', properties_types)]
#
#         elif py_type == list:
#             # get schema "items" object
#             schema_items = schema_object.items
#             return typing.List[cls._get_type(schema_items)]
#
#     @classmethod
#     def add(cls, name, schema: models.Schema):
#         if schema.allOf:
#             data_types = []
#             for all_of_schema in schema.allOf:
#                 if all_of_schema.ref:
#                     ref_name = all_of_schema.ref.split('/')[-1]
#                     cls.add(ref_name, resolvers.Ref(all_of_schema.ref, '/home/kobayashi/Documents/repos/mockingpy/openapi.yaml').resolve())
#                     data_types.append(cls.get(ref_name))
#                 else:
#                     additional_name = name + 'Additional'
#                     cls.add(additional_name, all_of_schema)
#                     data_types.append(cls.get(additional_name))
#
#             dynamic_response_model = type(name, (pydantic.BaseModel,), {'__root__': typing.Union[*data_types]})
#         else:
#             if schema.type != 'object':
#                 raise RuntimeError(f'Response models refers to "object" type, not "{schema.type}"')
#             model_properties = {}
#             for schema_property in schema.properties:
#                 model_properties[schema_property] = cls._get_type(schema.properties.get(schema_property))
#             dynamic_response_model = type(name, (pydantic.BaseModel,), model_properties)
#         setattr(cls, name, dynamic_response_model)
#         return getattr(cls, name)
#
#     @classmethod
#     def get(cls, name):
#         return getattr(cls, name)
