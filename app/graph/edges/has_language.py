from app.graph.edges import Edge


TextHasLanguage = Edge(
    name="Text_hasLanguage",
    from_node="Text",
    to_node="Language",
    metadata=["name STRING"],
    duckdb_query="""
    SELECT
        "H-ID" as "from",
        "language_COLUMN TRM-ID" as "to",
        'hasLanguage' as name
    FROM TextTable
    WHERE language_COLUMN is not null
""",
)
