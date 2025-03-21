import click
import importlib.metadata

from app.cli.pivot_commands import pivot
from app.cli.refresh_db_commands import refresh_db


__identifier__ = importlib.metadata.version("lostma-tei")


@click.group()
@click.version_option(__identifier__)
def cli():
    pass


if __name__ == "__main__":
    cli()


cli.add_command(refresh_db)
cli.add_command(pivot)
