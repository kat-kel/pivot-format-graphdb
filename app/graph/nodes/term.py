from app.graph.nodes import Node, Metadata

TERM_METADATA = [
    Metadata(
        label="id",
        type="INT",
    ),
    Metadata(
        label="name",
        type="STRING",
    ),
    Metadata(
        label="code",
        type="STRING",
    ),
    Metadata(
        label="description",
        type="STRING",
    ),
    Metadata(
        label="url",
        type="STRING",
    ),
]


Language = Node(
    label="Language",
    pk="id",
    metadata=TERM_METADATA,
    duckdb_query="""
    SELECT
        trm_ID as id,
        ANY_VALUE(trm_Label) as name,
        ANY_VALUE(trm_Code) as code,
        ANY_VALUE(trm_Description) as description,
        ANY_VALUE(trm_SemanticReferenceURL) as url
    FROM trm
    JOIN TextTable tt ON trm.trm_ID = tt."language_COLUMN TRM-ID"
    GROUP BY trm_ID
""",
)
