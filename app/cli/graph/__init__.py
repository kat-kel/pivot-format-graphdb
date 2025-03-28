import click

from .build_gexf import build_gexf, build_graph


@click.group("graph")
def graph():
    pass


graph.add_command(build_gexf)
graph.add_command(build_graph)
