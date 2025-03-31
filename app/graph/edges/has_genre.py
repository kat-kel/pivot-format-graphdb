from app.graph.edges import Edge, EdgeRelation

TextHasGenre = Edge(
    table_name="HAS_GENRE",
    relations=[
        EdgeRelation(
            from_node="Text",
            to_node="Genre",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    "specific_genre H-ID" as "to"
                FROM TextTable
                WHERE "specific_genre H-ID" IS NOT NULL
            """,
        )
    ],
)
