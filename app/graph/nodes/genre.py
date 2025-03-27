from app.graph.nodes import Node, Property


Genre = Node(
    name="Genre",
    pk="id",
    metadata=[
        Property(name="id", type="INT"),
        Property(name="name", type="STRING"),
        Property(name="alternative_names", type="STRING[]"),
        Property(name="description", type="STRING"),
        Property(name="described_at_URL", type="STRING[]"),
    ],
    duckdb_query="""
SELECT
    "H-ID" as id,
    preferred_name as name,
    alternative_names,
    description,
    described_at_URL
FROM Genre
""",
)
