import re

import jsonref

from loggers import main_logger


def resolve_refs(uri):
    with open(uri) as fp:
        return jsonref.load(fp, loader=jsonref.jsonloader)


def resolve_path(paths, url):
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

    return None
