import unittest

import dynamic

schema_example = {
    "type": "object",
    "required": [
        "name"
    ],
    "properties": {
        "name": {
            "type": "string"
        },
        "address": {
            "type": "object",
            "required": [
                "name"
            ],
            "properties": {
                "name": {
                    "type": "string"
                },
                # "address": {
                #   "$ref": "#/components/schemas/Address"
                # },
                "age": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 0
                }
            },
        },
        "age": {
            "type": "integer",
            "format": "int32",
            "minimum": 0
        }
    },
}

operation_example = {
    "description": "Returns all pets from the system that the user has access to",
    "responses": {
        "200": {
            "description": "A list of pets.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/pet"
                        }
                    }
                }
            }
        }
    }
}



operation_object_example = {
    "description": "Returns all pets from the system that the user has access to",
    "responses": {
        "200": {
            "description": "A list of pets.",
            "content": {
                "application/json": {
                    "schema": {
                        schema_example
                    }
                }
            }
        }
    }
}




class TestPathOperation(unittest.TestCase):

    def test_add(self):
        # self.assertEqual('foo'.upper(), 'FOO')
        print(dynamic.DynamicPathOperations.add('/dupa', 'get', operation_example))
        print(dynamic.DynamicPathOperations.add('/dupa', 'get', operation_object_example))


class TestResponseModel(unittest.TestCase):

    def test_add(self):
        print(dynamic.DynamicResponseModels.add('dupa', schema_example).name)
        print(dynamic.DynamicResponseModels.add('dupa', schema_example).address)


if __name__ == '__main__':
    unittest.main()
