from fastapi.openapi import models
from openapi_spec_validator import validate_spec

from openapi import resolvers


def load_document(document_path):
    data = resolvers.resolve_refs(document_path)
    validate_spec(data)
    data = models.OpenAPI(**data)
    return data
