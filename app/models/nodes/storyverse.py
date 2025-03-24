from . import Node

Storyverse = Node(
    name="Storyverse",
    duckdb_query="""
    SELECT
        "H-ID" as id,
        preferred_name as name,
        alternative_names,
        described_at_URL
    FROM Storyverse
    """,
    pk="id",
    metadata=[
        "id INT",
        "name STRING",
        "alternative_names STRING[]",
        "described_at_URL STRING[]",
    ],
)
