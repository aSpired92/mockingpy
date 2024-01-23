from fastapi.openapi import models
from openapi_spec_validator import validate_spec

import args
from openapi import resolvers


def load_document():
    """
    Pulls and validates documentation, resolves all references
    :return: Returns a documentation object
    """

    document_path = args.document_path
    data = resolvers.resolve_refs(document_path)
    validate_spec(data)
    data = models.OpenAPI(**data)
    return data
