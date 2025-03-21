import click

from .texts import pivot_all_texts


@click.group()
def pivot():
    pass


pivot.add_command(pivot_all_texts)
