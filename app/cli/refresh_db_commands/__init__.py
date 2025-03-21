import click

from .heurist_download import download


@click.group("heurist")
def refresh_db():
    pass


refresh_db.add_command(download)
