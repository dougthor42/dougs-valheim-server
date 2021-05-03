# -*- coding: utf-8 -*-
import logging

LOG_FMT = (
    "%(asctime)s"
    "|%(levelname)-8.8s"
    "|%(module)-8.8s"
    "|%(lineno)4d"
    "|%(funcName)-16.16s"
    "|%(message)s"
)
DATE_FMT = "%Y-%m-%dT%H-%M-%S"

logger = logging.getLogger("dougs_valheim_server")

_formatter = logging.Formatter(LOG_FMT)
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
