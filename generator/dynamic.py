import math
import random
import sys
from _decimal import Decimal

import rstr
from fastapi.openapi import models

from loggers import main_logger
from openapi.datatypes import Integer, Int32, Int64, Float, Double, Number, String, Date, DateTime, Password, Byte, \
    Binary

# TODO: logger with data information
# TODO: use enum for match case data type


def generate_endpoint(method_object):
    """
    Generuje klasę z metodą, której można użyć jako 'endpoint' przy dodawaniu ścieżki do API.
    Metoda jest w klasie _Dynamo, aby można było zapisać obiekt operacji, na którym ta metoda bazuje

    :param method_object: Obiekt operacji z dokumentacji API
    :return: Zwraca funkcję z instancji klasy
    """

    class _Dynamo:
        """
        (TO ŻYJE :D)
        """

        def __init__(self):
            self.method_object = method_object

        def endpoint(self):
            """
            Uniwersalna metoda endpoint-a, która na bazie obiektu operacji generuje losowe dane według schematu
            :return: Zwraca losowe dane
            """

            operation = self.method_object

            status_200 = operation.responses.get('200')
            content = status_200.content
            application_json = content.get("application/json")

            schema: models.Schema = application_json.schema_
            response_type = schema.type

            if schema.nullable:
                return None

            match response_type:
                case 'integer' | 'number':
                    return _generate_numeric(schema)
                case 'string':
                    return _generate_string(schema)
                case _:
                    raise RuntimeError(f'Unknown response type: {response_type}')

    return _Dynamo().endpoint


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
