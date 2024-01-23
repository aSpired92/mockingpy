# mockingpy

Python 3.11 mocking server based on FastApi and OpenAPI libraries

## Usage

To install project requirements:
```shell
pip install -r requirements.txt
```

To run the server
```shell
python main.py -p path/to/openapi/document [OPTIONS]
```

### Options

```shell
options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Document file path
  -r, --reload          Reloads when changes in document detected
  -a ADDRESS, --address ADDRESS
                        Overrides the document server host url
  -d, --debug           Debug mode. Reload server when changes in python files are detected
  -l {critical,error,warning,info,debug,trace}, --log-level {critical,error,warning,info,debug,trace}
                        Log level
```