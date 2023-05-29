import logging

logger = logging.getLogger("qoi_logger")
loglevel = "DEBUG"
logger.setLevel(loglevel)
handler = logging.StreamHandler()
handler.setLevel(loglevel)
format = '%(levelname)s - %(filename)s - %(funcName)s: %(message)s'
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)
