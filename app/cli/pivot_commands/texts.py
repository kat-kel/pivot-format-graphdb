import click

# from app import OUTDIR_PATH

# from app.tei_models.text.builder import TextTreeBuilder
# from rich.progress import (
#     Progress,
#     BarColumn,
#     TextColumn,
#     TimeElapsedColumn,
#     MofNCompleteColumn,
# )


@click.command("texts")
@click.option(
    "--database",
    required=False,
    help="If not using a .env file for storing the database file's location, \
        declare the file path.",
)
@click.option(
    "--outdir",
    required=False,
    help="If not using a .env file for storing the location of the directory \
        for the output TEI files, declare the directory path.",
)
def pivot_all_texts(database: str | None, outdir: str | None):
    # Connect to the dumped Heurist database.
    print("in development...")
