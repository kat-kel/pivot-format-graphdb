from app.graph.edges import Edge, EdgeRelation

GenreHasParent = Edge(
    table_name="HAS_PARENT",
    relations=[
        EdgeRelation(
            from_node="Genre",
            to_node="Genre",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    "parent_genre H-ID" as "to"
                FROM Genre
                WHERE "parent_genre H-ID" IS NOT NULL
                """,
        )
    ],
)
