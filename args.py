import argparse


_parser = argparse.ArgumentParser(
        prog='mockingpy',
        description='Python mocking server based on FastApi and OpenAPI libraries',
    )

_parser.add_argument('-p', '--path', help="Document file path", required=True)
_parser.add_argument(
    '-r', '--reload', action='store_true', help="Reloads when changes in document detected"
)
_parser.add_argument('-a', '--address', help="Overrides the document server host url")
_parser.add_argument(
    '-d', '--debug', action='store_true',
    help="Debug mode. Reload server when changes in python files are detected"
)
_parser.add_argument(
    '-l', '--log-level', choices=['critical', 'error', 'warning', 'info', 'debug', 'trace'],
    help="Log level", default='info'
)

list_ = vars(_parser.parse_args())

document_path = list_.get('path')
reload = list_.get('reload')
host = list_.get('address')
debug = list_.get('debug')
log_level = list_.get('log_level')
