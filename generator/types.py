import random

from fastapi.openapi import models

from openapi.datatypes import Int32, Int64, Float, Double, get_type_by_name








def generate_int32(schema: models.Schema) -> Int32:
    return Int32(random.randint(Int32.min, Int32.max))


def generate_int64(schema) -> Int64:
    return Int64(random.randint(Int64.min, Int64.max))


def generate_float(schema) -> Float:
    return Float(random.uniform(Float.min, Float.max))

def generate_double(schema) -> Double:
    return random.uniform(1.5, 1.9)

def generate_string(schema):
    return random.randint()