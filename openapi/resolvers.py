import jsonref


def resolve_refs(uri):
    with open(uri) as fp:
        return jsonref.load(fp, loader=jsonref.jsonloader)


def resolve_path(paths, url):

    url_parts = url.split('/')

    for path in paths:
        path_parts = path.split('/')
        path_object = paths.get(path)

        if len(path_parts) == len(url_parts):
            print(url_parts)
            print(path_parts)
            for i in range(len(path_parts)):
                path_part: str = path_parts[i]
                url_part: str = url_parts[i]
                if path_part.startswith('{') and path_part.endswith('}'):
                    continue
                if path_part != url_part:
                    print('wrong')
                    break


    return paths.get(url)
