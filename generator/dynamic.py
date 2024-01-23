import math
import random
import sys
from _decimal import Decimal

import rstr
from fastapi.openapi import models

from loggers import main_logger
from openapi.datatypes import Integer, Int32, Int64, Float, Double, Number, String, Date, DateTime, Password, Byte, \
    Binary
from openapi.enums import ResponseType


# TODO: Add logger with data information
# TODO: Add support for other statuses (400, 404, etc.)
# TODO: Add command arguments (nullable, errors)



def generate_endpoint(method_object):
    """
    Generates a class with a method that can be used as an 'endpoint' parameter when adding a path to the API.
    The method is in the _Dynamo class so that you can save the operation object on which the method is based
    """

    class _Dynamo:
        """
        It's alive :D
        """

        def __init__(self):
            self.method_object = method_object

        def endpoint(self):
            """
            A universal endpoint method that generates random data based on the operation object according to the scheme
            :return: Returns random data
            """

            operation = self.method_object

            status_200 = operation.responses.get('200')
            content = status_200.content
            application_json = content.get("application/json")

            schema: models.Schema = application_json.schema_

            if schema.nullable:
                return None

            return _generate_response(schema)

    return _Dynamo().endpoint


def _generate_response(schema: models.Schema):
    response_type = schema.type
    match response_type:
        case ResponseType.INTEGER.value | ResponseType.NUMBER.value:
            return _generate_numeric(schema)
        case ResponseType.STRING.value:
            return _generate_string(schema)
        case ResponseType.OBJECT.value:
            return _generate_object(schema)
        case ResponseType.ARRAY.value:
            return _generate_array(schema)
        case _:
            raise RuntimeError(f'Unknown response type: {response_type}')


def _generate_string(schema: models.Schema):
    data_type = {
        None: String,
        'date': Date,
        'date-time': DateTime,
        'password': Password,
        'byte': Byte,
        'binary': Binary,
    }.get(schema.format)

    pattern = data_type.regex or schema.pattern
    if pattern:
        return rstr.xeger(pattern)

    minimum = schema.minLength or None
    maximum = schema.maxLength or None

    if maximum and not minimum:
        return rstr.rstr(data_type.characters, maximum)
    elif maximum and minimum:
        return rstr.rstr(data_type.characters, minimum, maximum)

    return rstr.rstr(data_type.characters)


def _generate_object(schema: models.Schema):
    return {key: _generate_response(schema_object) for key, schema_object in schema.properties.items()}


def _generate_array(schema: models.Schema):
    return [_generate_response(schema.items) for _ in list(range(random.randrange(3, 10)))]


def _generate_numeric(schema: models.Schema):
    if (
        schema.minimum is not None and schema.maximum is not None and
        schema.minimum == schema.minimum and (schema.exclusiveMaximum or schema.exclusiveMinimum)
    ):
        raise RuntimeError('No possible number for equal limits and exclusive limit')

    # Tworzy bazowe dane dla podanych typów
    match schema.type:
        case 'integer':
            data_type = {
                None: Integer,
                'int32': Int32,
                'int64': Int64
            }.get(schema.format)

            step = 1

            def calculate(minim, maxim, multiple):
                return random.randrange(int(minim), int(maxim), int(multiple))

        case 'number':
            data_type = {
                None: Number,
                'float': Float,
                'double': Double
            }.get(schema.format)

            step = Decimal(sys.float_info.epsilon)

            def calculate(minim, maxim, multiple):
                return int((minim + (maxim - minim) * Decimal(random.random())) / multiple) * multiple

        case _:
            raise RuntimeError(f'Unknown response type: {schema.type}')

    print(step)

    if schema.minimum is not None:
        minimum = Decimal(schema.minimum)
        if schema.exclusiveMinimum:
            minimum += Decimal(step)
    else:
        minimum = data_type.min

    if schema.maximum is not None:
        maximum = Decimal(schema.maximum)
        if schema.exclusiveMaximum:
            maximum -= Decimal(step)
    else:
        maximum = data_type.max

    multiple_of = Decimal(schema.multipleOf or step)

    minimum = math.ceil(minimum / multiple_of) * multiple_of
    maximum = math.floor(maximum / multiple_of) * multiple_of

    return calculate(minimum, maximum, multiple_of)
