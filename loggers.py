import logging

import args

if args.log_level:
    level = args.log_level.upper()
else:
    level = logging.INFO

logging.basicConfig(level=level)
main_logger = logging.getLogger("uvicorn")
main_logger.setLevel(level)
