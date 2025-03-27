from app.graph.edges import Edge


TextHasGenre = Edge(
    name="Text_hasGenre",
    from_node="Text",
    to_node="Genre",
    metadata=["name STRING"],
    duckdb_query="""
SELECT
    "H-ID" as "from",
    "specific_genre H-ID" as "to",
    'hasGenre' as name
FROM TextTable
WHERE "specific_genre H-ID" IS NOT NULL
""",
)
