import apps
import interfaces

METHODS = {
    'get': apps.fastapi.get
}

TYPES = {
    'object': {
        'type': object,
        'nested': True,
    },
    'string': {
        'type': str,
        'nested': False
    },
    'array': {
        'type': list,
        'nested': True
    },
    'integer': {
        'type': int,
        'nested': False
    },
}
