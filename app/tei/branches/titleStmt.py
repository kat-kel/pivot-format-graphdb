from lxml import etree

from app.tei.branches.respStmt import list_resp_persons
from app.tei.fetchers.language import fetch_language
from app.tei.fetchers.text_alternative_titles import fetch_alternative_title
from app.tei.fetchers.text_title import fetch_title
from app.tei.text_xml_parser import TitleStmtParser
from kuzu import Connection


def build_titleStmt(conn: Connection, text_id: int, root: TitleStmtParser):
    # Set the titleStmt's <title>
    data = fetch_title(conn=conn, id=text_id)
    full_title = f'Metadata encoding of "{data}"'
    root.title.text = full_title

    # Set alternative titles
    parent = root.title
    for alt_title in fetch_alternative_title(conn=conn, id=text_id):
        node = etree.Element("title", type="alt")
        node.text = alt_title
        parent.append(node)

    # Set the titleStmt's <respStmt>
    language = fetch_language(conn=conn, id=text_id)
    people = list_resp_persons(lang=language)
    parent = root.respStmt
    for person in people:
        n = etree.SubElement(parent, "name")
        n.text = person.name
        n = etree.SubElement(parent, "resp")
        n.text = person.role
