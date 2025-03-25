from app.models.nodes import Node, Property


Text = Node(
    name="Text",
    pk="id",
    metadata=[
        Property(name="id", type="INT"),
        Property(name="name", type="STRING"),
        Property(name="language", type="STRING"),
        Property(name="form", type="STRING"),
        Property(name="is_hypothetical", type="BOOLEAN"),
        Property(name="hypothesis", type="STRING"),
        Property(name="alternative_names", type="STRING[]"),
        Property(name="is_peripheral", type="BOOLEAN"),
        Property(name="length", type="FLOAT"),
        Property(name="length_freetext", type="STRING"),
        Property(name="verse_type", type="STRING"),
        Property(name="rhyme_type", type="STRING"),
        Property(name="stanza_type", type="STRING"),
        Property(name="tradition_status", type="STRING"),
        Property(name="has_lost_older_version", type="BOOLEAN"),
        Property(name="lost_older_version_freetext", type="STRING"),
        Property(name="rewritings_freetext", type="STRING"),
        Property(name="note", type="STRING"),
        Property(name="creation_earliest_date", type="DATE"),
        Property(name="creation_latest_date", type="DATE"),
        Property(name="creation_date_certainty", type="STRING"),
        Property(name="creation_date_source", type="STRING"),
        Property(name="creation_date_freetext", type="STRING"),
        Property(name="described_at_URL", type="STRING[]"),
    ],
    duckdb_query="""
    SELECT
        "H-ID" as id,
        preferred_name as name,
        language_COLUMN as "language",
        literary_form as "form",
        case when is_hypothetical like 'Yes' then True else False end as \
is_hypothetical,
        claim_freetext as hypothesis,
        alternative_names,
        case when peripheral like 'Yes' then True else False end as is_peripheral,
        length,
        length_freetext,
        verse_type,
        rhyme_type,
        Stanza_type as stanza_type,
        tradition_status,
        case when has_lost_older_version like 'Yes' then True else False end as \
has_lost_older_version,
        ancient_translations_freetext as lost_older_version_freetext,
        rewritings_freetext,
        "note",
        case when length(date_of_creation) > 0 then date_of_creation[1] else null end \
as creation_earliest_date,
        case when length(date_of_creation) > 1 then date_of_creation[2] else null end \
as creation_latest_date,
        date_of_creation_certainty as creation_date_certainty,
        date_of_creation_source as creation_date_source,
        date_freetext as creation_date_freetext,
        described_at_URL
    FROM TextTable
""",
)
