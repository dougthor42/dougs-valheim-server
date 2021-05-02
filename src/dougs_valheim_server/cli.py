import click


@click.group()
def main():
    print("main")


@main.command()
def status():
    print("status")


@main.command()
def stop():
    print("stop")


@main.command()
def start():
    print("start")
