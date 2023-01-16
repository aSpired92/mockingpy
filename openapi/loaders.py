from fastapi.openapi import models
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename

from openapi import resolvers


class DocumentLoader:

    @staticmethod
    def load(document_path):
        data = resolvers.resolve(document_path)
        validate_spec(data)
        data = models.OpenAPI(**data)
        return data
