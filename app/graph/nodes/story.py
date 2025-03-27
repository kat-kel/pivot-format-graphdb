from app.graph.nodes import Node, Property


Story = Node(
    name="Story",
    pk="id",
    metadata=[
        Property(name="id", type="INT"),
        Property(name="name", type="STRING"),
        Property(name="alternative_names", type="STRING[]"),
        Property(name="matter", type="STRING"),
        Property(name="peripheral", type="STRING"),
        Property(name="described_at_URL", type="STRING[]"),
    ],
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
)
