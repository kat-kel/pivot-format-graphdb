import click

from .build_gexf import build_gexf


@click.group("graph")
def graph():
    pass


graph.add_command(build_gexf)
