import os
import typing

from fastapi.openapi import models

from openapi.loaders import DocumentLoader


class Ref:

    def __init__(self, ref: str, referrer_path: str):
        self.ref = ref
        self.referrer = referrer_path

    def resolve(self) -> models.Schema:
        ref_parts = self.ref.split('#')
        temp_path = self.referrer
        if ref_parts[0]:
            for module in ref_parts[0].split('/'):
                temp_path = os.path.join(temp_path, module)
        current_object = DocumentLoader.load(temp_path)
        for module in ref_parts[1].split('/'):
            if module:
                if type(current_object) == dict:
                    current_object = current_object.get(module)
                else:
                    current_object = getattr(current_object, module)
        print(current_object)
        return current_object

