from app.models.edges import Edge


StoryIsPartOfStoryverse = Edge(
    name="Story_isPartOf",
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
    name="Storyverse_isPartOf",
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
