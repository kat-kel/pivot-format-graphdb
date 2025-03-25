import click
import importlib.metadata

from app.cli.pivot import pivot
from app.cli.heurist import refresh_db
from app.cli.graph import graph

__identifier__ = importlib.metadata.version("lostma-tei")


@click.group()
@click.version_option(__identifier__)
def cli():
    pass


if __name__ == "__main__":
    cli()


cli.add_command(refresh_db)
cli.add_command(pivot)
cli.add_command(graph)
