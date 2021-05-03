# -*- coding: utf-8 -*-
import logging

import click

from . import logger
from . import main

LOG_LEVELS = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


@click.group()
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    if verbose > 2:
        verbose = 2

    logger.setLevel(LOG_LEVELS[verbose])


@cli.command()
def status():
    logger.debug("command line: status")
    instance = main._get_instance()
    status = main.get_status(instance)
    ip = main.get_ip(instance)
    main.print_status(status, ip)


@cli.command()
def stop():
    logger.debug("command line: stop")
    instance = main._get_instance()
    main.stop_instance(instance)


@cli.command()
def start():
    logger.debug("command line: start")
    instance = main._get_instance()
    main.start_instance(instance)
