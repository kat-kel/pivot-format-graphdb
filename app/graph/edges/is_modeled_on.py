from app.graph.edges import Edge, EdgeRelation

IsModeledOn = Edge(
    table_name="IS_MODELED_ON",
    relations=[
        EdgeRelation(
            from_node="Story",
            to_node="Story",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    unnest("is_modeled_on H-ID") as "to"
                FROM Story
                WHERE "is_modeled_on H-ID" != []
                """,
        )
    ],
)
