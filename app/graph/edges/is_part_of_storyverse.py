from app.graph.edges import Edge, EdgeRelation

IsPartOfStoryverse = Edge(
    table_name="IS_PART_OF_STORYVERSE",
    relations=[
        EdgeRelation(
            from_node="Story",
            to_node="Storyverse",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    unnest("is_part_of_storyverse H-ID") as "to"
                FROM Story
                WHERE "is_part_of_storyverse H-ID" != []
            """,
        ),
        EdgeRelation(
            from_node="Storyverse",
            to_node="Storyverse",
            duckdb_query="""
                SELECT
                    "H-ID" as "from",
                    unnest("member_of_cycle H-ID") as "to"
                FROM Storyverse
                WHERE "member_of_cycle H-ID" != []
            """,
        ),
    ],
)
