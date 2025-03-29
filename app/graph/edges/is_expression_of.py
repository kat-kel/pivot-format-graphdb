from app.graph.edges import Edge

TextIsExpressionOf = Edge(
    table_name="Text_isExpressionOf",
    from_node="Text",
    to_node="Story",
    metadata=["name STRING"],
    duckdb_query="""
    SELECT
        "H-ID" as "from",
        unnest("is_expression_of H-ID") as "to",
        'isExressionOf' as name
    FROM TextTable
    WHERE "is_expression_of H-ID" != []
    """,
)
