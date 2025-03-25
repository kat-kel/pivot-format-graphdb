from app.models.nodes import Node, Property

TERM_METADATA = [
    Property(name="id", type="INT"),
    Property(name="name", type="STRING"),
    Property(name="code", type="STRING"),
    Property(name="description", type="STRING"),
    Property(name="url", type="STRING"),
]


Language = Node(
    name="Language",
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
