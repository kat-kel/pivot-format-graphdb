from app.graph.nodes import Node, Metadata

Story = Node(
    label="Story",
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
            label="matter",
            type="STRING",
        ),
        Metadata(
            label="peripheral",
            type="STRING",
        ),
        Metadata(
            label="described_at_URL",
            type="STRING[]",
        ),
    ],
    table="Story",
)
