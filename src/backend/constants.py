from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent.joinpath("heurist.db")


class HeuristDB:
    digitization = "Digitization"
    document = "DocumentTable"
    footnote = "Footnote"
    genre = "Genre"
    images = "Images"
    part = "Part"
    physDesc = "PhysDesc"
    repository = "Repository"
    scripta = "Scripta"
    stemma = "Stemma"
    story = "Story"
    storyverse = "Storyverse"
    text = "TextTable"
    witness = "Witness"
