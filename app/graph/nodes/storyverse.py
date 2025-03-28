from app.graph.nodes import Node, Metadata


Storyverse = Node(
    label="Storyverse",
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
