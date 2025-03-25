import click
import kuzu
import duckdb
import shutil

from app import KUZU_DB, HEURIST_DB
from app.utils.write_gexf import write_gexf
from app.models.builders import create_all_edges, create_all_nodes


@click.command("gexf")
@click.argument("outfile")
def build_gexf(outfile: str):
    shutil.rmtree(KUZU_DB)
    db = kuzu.Database(KUZU_DB)
    kconn = kuzu.Connection(db)
    dconn = duckdb.connect(HEURIST_DB)

    create_all_nodes(kconn=kconn, dconn=dconn)
    create_all_edges(kconn=kconn, dconn=dconn)

    query = "MATCH (n)-[r]->(m) RETURN n,r,m"
    res = kconn.execute(query=query)
    write_gexf(res=res, filepath=outfile)
