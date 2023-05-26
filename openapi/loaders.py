from fastapi.openapi import models
from openapi_spec_validator import validate_spec

from openapi import resolvers


def load_document(document_path):
    """
    Zaciąga i waliduje dokumentację, rozwiązuje wszystkie referencje

    :param document_path: Ścieżka do pliku
    :return: Zwraca obiekt dokumentacji
    """
    data = resolvers.resolve_refs(document_path)
    validate_spec(data)
    data = models.OpenAPI(**data)
    return data
