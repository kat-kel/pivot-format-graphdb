from app.graph.edges import Edge, EdgeRelation

TextIsExpressionOf = Edge(
    table_name="IS_EXPRESSION_OF",
    relations=[
        EdgeRelation(
            from_node="Text",
            to_node="Story",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    unnest("is_expression_of H-ID") as "to"
                FROM TextTable
                WHERE "is_expression_of H-ID" != []
                """,
        )
    ],
)
