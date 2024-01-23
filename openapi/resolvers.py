import re
import urllib
from urllib.parse import urlsplit

import jsonref
from fastapi.openapi import models

from loggers import main_logger


def resolve_refs(uri):
    """
    Resolve all references in the documentation file

    :param uri: Path to the documentation file
    :return: Returns the same document with resolved references
    """
    with open(uri) as fp:
        return jsonref.load(fp, loader=jsonref.jsonloader)


def resolve_methods(path_object):
    """
    Resolves all methods from path_object

    :param path_object: OpenAPI path object
    :return: Dictionary of method objects
    """
    return {method: getattr(path_object, method) for method in [
        'get', 'post', 'put', 'delete', 'options', 'head', 'patch', 'trace'
    ] if getattr(path_object, method)}
