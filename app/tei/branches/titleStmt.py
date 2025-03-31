from lxml import etree

from app.tei.builders.respStmt import list_resp_persons
from app.tei.fetchers.language import fetch_language
from app.tei.fetchers.text_alternative_titles import fetch_alternative_title
from app.tei.fetchers.text_title import fetch_title
from app.tei.text_xml_parser import ParserTitleStmt
from kuzu import Connection


def build_titleStmt(conn: Connection, text_id: int, root: ParserTitleStmt):
    # Set the main title
    data = fetch_title(conn=conn, id=text_id)
    main = etree.SubElement(root.title, "title", type="main")
    main.text = data
    sub = etree.SubElement(root.title, "title", type="sub")
    sub.text = "Encoding of Metadata"

    # Set alternative titles
    parent = root.title
    alt_titles = fetch_alternative_title(conn=conn, id=text_id)
    for alt_title in alt_titles:
        node = etree.Element("title", type="alt")
        node.text = alt_title
        parent.addnext(node)

    # Set the titleStmt's <respStmt>
    language = fetch_language(conn=conn, id=text_id)
    people = list_resp_persons(lang=language)
    parent = root.respStmt
    for person in people:
        n = etree.SubElement(parent, "name")
        n.text = person.name
        n = etree.SubElement(parent, "resp")
        n.text = person.role
