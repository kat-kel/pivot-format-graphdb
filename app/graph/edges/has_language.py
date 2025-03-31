from app.graph.edges import Edge, EdgeRelation

TextHasLanguage = Edge(
    table_name="HAS_LANGAUGE",
    relations=[
        EdgeRelation(
            from_node="Text",
            to_node="Language",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    CAST("language_COLUMN TRM-ID" AS INT64) as "to"
                FROM TextTable
                WHERE "language_COLUMN TRM-ID" is not null
            """,
        )
    ],
)
