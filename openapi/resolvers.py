import re

import jsonref
from fastapi.openapi import models

from loggers import main_logger


def resolve_refs(uri):
    """
    Rozwiązuje wszystkie referencje w pliku dokumentacji

    :param uri: Ścieżka do pliku dokumentacji
    :return: Zwraca ten sam dokument z rozwiązanymi referencjami
    """
    with open(uri) as fp:
        return jsonref.load(fp, loader=jsonref.jsonloader)


def resolve_path(paths, url) -> models.PathItem:
    """
    Wyszukuje ścieżkę z dokumentacji na bazie podanego adresu
    Podmienia parametry ścieżki na regexy tak, aby można było przyrównać je do adresu zapytania

    :param paths: lista ścieżek do przeszukania
    :param url: adres
    :return: Obiekt ścieżki
    """

    for path, path_object in paths.items():
        main_logger.debug(path)

        regex_path = re.sub('{.*?}', '.+', path, flags=re.DOTALL).replace('/', '\\/')

        main_logger.debug(regex_path)
        if re.match(f'{regex_path}', url):
            return path_object

    raise RuntimeError('Path not found')


def resolve_methods(path_object):
    """
    TODO: Dokończyć komentarze

    :param path_object:
    :return:
    """
    return {method: getattr(path_object, method) for method in [
        'get', 'post', 'put', 'delete', 'options', 'head', 'patch', 'trace'
    ] if getattr(path_object, method)}
