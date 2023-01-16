import json
import os

import jsonref


def _loader(uri):
    # custom ref resolving
    return jsonref.jsonloader(uri)


def resolve(uri):
    with open(uri) as fp:
        return jsonref.load(fp, loader=_loader)

