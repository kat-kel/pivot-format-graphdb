from app.graph.edges import Edge

StoryIsPartOfStoryverse = Edge(
    table_name="STORY_IS_PART_OF",
    from_node="Story",
    to_node="Storyverse",
    metadata=["name STRING"],
    duckdb_query="""
    SELECT
        "H-ID" as "from",
        unnest("is_part_of_storyverse H-ID") as "to",
        'isPartOfStoryverse' as name
    FROM Story
    WHERE "is_part_of_storyverse H-ID" != []
    """,
)


StoryverseIsPartOfStoryverse = Edge(
    table_name="STORYVERSE_IS_PART_OF",
    duckdb_query="""
    SELECT
        "H-ID" as "from",
        unnest("member_of_cycle H-ID") as "to",
        'isPartOfStoryverse' as name
    FROM Storyverse
    WHERE "member_of_cycle H-ID" != []
    """,
    from_node="Storyverse",
    to_node="Storyverse",
    metadata=["name STRING"],
)
