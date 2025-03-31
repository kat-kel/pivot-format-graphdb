from app.graph.edges import Edge, EdgeRelation

WitnessIsManifestationOf = Edge(
    table_name="IS_MANIFESTATION_OF",
    relations=[
        EdgeRelation(
            from_node="Witness",
            to_node="Text",
            duckdb_query="""
                SELECT
                    "H-ID" as "to",
                    "is_manifestation_of H-ID" as "from"
                FROM Witness
                WHERE "is_manifestation_of H-ID" IS NOT NULL
                """,
        )
    ],
)
