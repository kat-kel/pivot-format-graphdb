from app.models.nodes import Node


Story = Node(
    name="Story",
    duckdb_query="""
        SELECT
            "H-ID" as id,
            preferred_name as name,
            alternative_names,
            matter,
            peripheral,
            described_at_URL
        FROM Story
    """,
    pk="id",
    metadata=[
        "id INT",
        "name STRING",
        "alternative_names STRING[]",
        "matter STRING",
        "peripheral STRING",
        "described_at_URL STRING[]",
    ],
)
