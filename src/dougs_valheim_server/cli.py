import click


@click.group()
def cli():
    print("cli")


@cli.command()
def status():
    print("status")


@cli.command()
def stop():
    print("stop")


@cli.command()
def start():
    print("start")
