from app.graph.nodes import Node, Property


Witness = Node(
    name="Witness",
    pk="id",
    metadata=[
        Property(name="id", type="INT"),
        Property(name="is_unobserved", type="BOOLEAN"),
        Property(name="hypothesis", type="STRING"),
        Property(name="preferred_siglum", type="STRING"),
        Property(name="alternative_sigla", type="STRING[]"),
        Property(name="status_witness", type="STRING"),
        Property(name="status_note", type="STRING"),
        Property(name="is_excerpt", type="BOOLEAN"),
        Property(name="creation_earliest_date", type="DATE"),
        Property(name="creation_latest_date", type="DATE"),
        Property(name="creation_date_temporal", type="STRING"),
        Property(name="creation_date_certainty", type="STRING"),
        Property(name="creation_date_source", type="STRING"),
        Property(name="creation_date_freetext", type="STRING"),
        Property(name="described_at_URL", type="STRING[]"),
    ],
    duckdb_query="""
    SELECT
        "H-ID" as id,
        case when is_unobserved like 'Yes' then True else False end is_unobserved,
        claim_freetext as hypothesis,
        preferred_siglum,
        alternative_sigla,
        status_witness,
        status_notes as status_note,
        case when is_excerpt like 'Yes' then True else False end is_excerpt,
        case when length(date_of_creation) > 0 then date_of_creation[1] else null end \
as creation_earliest_date,
        case when length(date_of_creation) > 1 then date_of_creation[2] else null end \
as creation_latest_date,
        date_of_creation_TEMPORAL as creation_date_temporal,
        date_of_creation_certainty as creation_date_certainty,
        date_of_creation_source as creation_date_source,
        date_freetext as creation_date_freetext,
        described_at_URL
    FROM Witness
    """,
)
