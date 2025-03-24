import click
from click import ClickException
from pathlib import Path
from app.database import DBConn
from app import OUTDIR_PATH

# from app.data_models.text import TextModel
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
    if database:
        db = DBConn(fp=database)
    else:
        db = DBConn()
    # Make the directory for the output TEI files
    if outdir:
        OUTDIR = Path(outdir)
    elif OUTDIR_PATH:
        OUTDIR = Path(OUTDIR_PATH)
    else:
        raise ClickException(
            "User must declare a directory for the generated TEI files."
        )
    OUTDIR.mkdir(exist_ok=True)

    # Select all the texts from the dumped Heurist database
    # rows = db.select_all('SELECT * FROM TextTable ORDER BY "H-ID"')

    # Iteratively build and write texts' TEI documents to the output directory.
    # with Progress(
    #     TextColumn("{task.description}"),
    #     BarColumn(),
    #     MofNCompleteColumn(),
    #     TimeElapsedColumn(),
    # ) as p:
    #     t = p.add_task("Transforming text metadata...", total=len(rows))
    #     for row in rows:
    #         data = TextModel.build_nested_dict(row_dict=row, db=db)
    #         model = TextModel.model_validate(data)
    #         fp = OUTDIR.joinpath(f"{model.xml_id}.xml")
    #         tree = TextTreeBuilder(text_data_model=model)
    #         tree.write(outfile=fp)
    #         p.advance(task_id=t)
