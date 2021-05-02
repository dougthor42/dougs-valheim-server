import click

from . import main


@click.group()
def cli():
    print("cli")


@cli.command()
def status():
    print("status")
    main.get_status()


@cli.command()
def stop():
    print("stop")


@cli.command()
def start():
    print("start")
