import re

import jsonref

from loggers import main_logger


def resolve_refs(uri):
    with open(uri) as fp:
        return jsonref.load(fp, loader=jsonref.jsonloader)


def resolve_path(paths, url):
    """
    Wyszukuje ścieżkę z dokumentacji na bazie podanego adresu

    :param paths: lista ścieżek do przeszukania
    :param url: adres
    :return: Obiekt ścieżki
    """

    # szukamy odpowiedniej ścieżki po adresie
    for path, path_object in paths.items():
        main_logger.debug(path)

        # jeśli ścieżka zawiera parametry, to je zastępujemy regexem
        regex_path = re.sub('{.*?}', '.+', path, flags=re.DOTALL).replace('/', '\\/')

        main_logger.debug(regex_path)
        if re.match(f'{regex_path}', url):
            return path_object

    # jeśli nie znaleziono odpowiedniej ścieżki, zwracamy None
    return None