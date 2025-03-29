from app.graph.nodes import Metadata, Node

Storyverse = Node(
    table_name="Storyverse",
    pk="id",
    metadata=[
        Metadata(
            label="id",
            col="H-ID",
            type="INT",
        ),
        Metadata(
            label="name",
            col="preferred_name",
            type="STRING",
        ),
        Metadata(
            label="alternative_names",
            type="STRING[]",
        ),
        Metadata(
            label="described_at_URL",
            type="STRING[]",
        ),
    ],
    table="Storyverse",
)
