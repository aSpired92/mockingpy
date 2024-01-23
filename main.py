from urllib.parse import urlsplit

import uvicorn

import args
from loggers import main_logger
from openapi import loaders

if __name__ == "__main__":
    """
    Preparation of arguments and uvicorn server
    """

    main_logger.debug(f'Arguments: {args.list_}')

    # Documentation loading
    document = loaders.load_document()

    main_logger.debug(f'Host argument: {args.host}')
    address = urlsplit(args.host or document.servers[0].url)

    if not address:
        raise ValueError("Server url has to be specified in the document servers object or \"-a\" argument")

    host = address.hostname
    port = address.port

    reload = False

    # Debug mode
    if args.debug:
        reload = True
        reload_excludes = None
    else:
        reload_excludes = ['*.py']

    # Reload mode
    if args.reload:
        reload = True
        reload_includes = [args.document_path]
    else:
        reload_includes = None

    # For the ability to expand basic arguments, uvicorn is run programmatically
    uvicorn.run(
        "generator.app:api",
        host=host,
        port=port,
        log_level=args.log_level,
        reload=reload,
        reload_includes=reload_includes,
        reload_excludes=reload_excludes
    )
