import logging

logging.basicConfig(level=logging.DEBUG)
main_logger = logging.getLogger("uvicorn")
main_logger.setLevel(logging.DEBUG)
