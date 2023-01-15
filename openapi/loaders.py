from fastapi.openapi import models
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename


class DocumentLoader:

    @staticmethod
    def load(document_path):
        data, _ = read_from_filename(document_path)
        validate_spec(data)
        data = models.OpenAPI(**data)
        return data
