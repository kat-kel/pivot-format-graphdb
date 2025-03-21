import click
import duckdb
from dotenv import find_dotenv, load_dotenv
import os

from app import DB_PATH
from heurist.api.client import HeuristAPIClient
from heurist.workflows.etl import extract_transform_load


def get_vars(*args) -> dict:
    load_dotenv(find_dotenv())
    db, login, password = args[0], args[1], args[2]
    if not db:
        db = os.getenv("DB_NAME")
    if not login:
        login = os.getenv("DB_LOGIN")
    if not password:
        password = os.getenv("DB_PASSWORD")
    return {"database_name": db, "login": login, "password": password}


RECORD_GROUP_NAMES = ["My record types", "Place, features", "People and organisations"]


@click.command("download")
@click.option("-d", "--database", type=click.STRING, required=False)
@click.option("-l", "--login", type=click.STRING, required=False)
@click.option("-p", "--password", type=click.STRING, required=False)
def download(database, login, password):
    kwargs = get_vars(database, login, password)
    client = HeuristAPIClient(**kwargs)
    conn = duckdb.connect(DB_PATH)
    extract_transform_load(
        client=client,
        duckdb_connection=conn,
        record_group_names=RECORD_GROUP_NAMES,
    )


if __name__ == "__main__":
    download()
