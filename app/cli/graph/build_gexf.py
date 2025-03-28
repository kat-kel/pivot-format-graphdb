import shutil
from pathlib import Path

import click
import duckdb
import kuzu
import rich
import rich.text
from rich.progress import Progress, SpinnerColumn, TextColumn

from app import HEURIST_DB, KUZU_DB
from app.graph.builders import create_all_edges, create_all_nodes
from app.utils.write_gexf import write_gexf


def build_command() -> kuzu.Connection:
    if not Path(HEURIST_DB).is_file():
        rich.print(rich.text.Text("Error.", style="red"))
        rich.print(f"No downloaded database file at '{HEURIST_DB}'.")
        rich.print("Run the command 'lostma-tei heurist download'.")
        rich.print("Exiting...")
        exit()

    with Progress(TextColumn("{task.description}"), SpinnerColumn()) as p:
        _ = p.add_task("Connecting to Heurist download...")
        dconn = duckdb.connect(HEURIST_DB)

    with Progress(TextColumn("{task.description}"), SpinnerColumn()) as p:
        _ = p.add_task("Rebuilding Kùzu database")
        if Path(KUZU_DB).is_dir():
            shutil.rmtree(KUZU_DB)
        db = kuzu.Database(KUZU_DB)
        kconn = kuzu.Connection(db)
        create_all_nodes(kconn=kconn, dconn=dconn)
        create_all_edges(kconn=kconn, dconn=dconn)
    return kconn


@click.command("build")
def build_graph():
    build_command()


@click.command("gexf")
@click.option("-n", "--node", multiple=True, type=click.STRING)
@click.argument("outfile")
def build_gexf(outfile: str, node: tuple[str]):
    kconn = build_command()
    if not node:
        query = "MATCH (n)-[r]->(m) RETURN n,r,m"
    else:
        nodes = ":".join(node)
        query = f"MATCH (n:{nodes})-[]->() RETURN *"
    res = kconn.execute(query=query)
    write_gexf(res=res, filepath=outfile)
