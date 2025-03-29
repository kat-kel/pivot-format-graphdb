from app.graph.edges import Edge

WitnessIsManifestationOf = Edge(
    table_name="Witness_isManifestationOf",
    from_node="Witness",
    to_node="Text",
    metadata=["name STRING"],
    duckdb_query="""
    SELECT
        "H-ID" as "to",
        "is_manifestation_of H-ID" as "from",
        'isManifestationOf' as name
    FROM Witness
    WHERE "is_manifestation_of H-ID" IS NOT NULL
    """,
)
