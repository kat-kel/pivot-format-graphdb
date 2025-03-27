from app.graph.edges import Edge


IsModeledOn = Edge(
    name="Sotry_isModeledOn",
    from_node="Story",
    to_node="Story",
    metadata=["name STRING"],
    duckdb_query="""
    SELECT
        "H-ID" as "from",
        unnest("is_modeled_on H-ID") as "to",
        'isModeledOn' as name
    FROM Story
    WHERE "is_modeled_on H-ID" != []
    """,
)
