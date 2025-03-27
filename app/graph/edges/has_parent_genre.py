from app.graph.edges import Edge


GenreHasParent = Edge(
    name="Genre_hasParent",
    from_node="Genre",
    to_node="Genre",
    metadata=["name STRING"],
    duckdb_query="""
SELECT
    "H-ID" as "from",
    "parent_genre H-ID" as "to",
    'hasParent' as name
FROM Genre
WHERE "parent_genre H-ID" IS NOT NULL
""",
)
