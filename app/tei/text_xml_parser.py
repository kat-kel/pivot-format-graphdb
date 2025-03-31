"""Class for navigating the base (empty) tree of the text's TEI document."""

from datetime import datetime

from lxml import etree

from app import TEXT_TEI_MODEL
from app.tei.find_node import find_node


class ParserTitleStmt:
    """Branch of XML tree at teiHeader/fileDesc/titleStmt."""

    def __init__(self, tree: etree.ElementTree):
        self.tree = tree

    @property
    def title(self) -> etree.Element:
        xpath = ".//tei:titleStmt/tei:title[@type='full']"
        return find_node(tree=self.tree, xpath=xpath)

    @property
    def respStmt(self) -> etree.Element:
        xpath = ".//tei:titleStmt/tei:respStmt"
        return find_node(tree=self.tree, xpath=xpath)


class ParserPublicationStmt:
    """Branch of XML tree at teiHeader/fileDesc/publicationStmt."""

    def __init__(self, tree: etree.ElementTree):
        self.tree = tree
        self.date.text = datetime.now().strftime("%Y-%m-%d")

    @property
    def date(self) -> etree.Element:
        xpath = ".//tei:publicationStmt/tei:date"
        return find_node(tree=self.tree, xpath=xpath)


class ParserEncodingDesc:
    """Branch of XML tree at teiHeader/encodingDesc."""

    def __init__(self, tree: etree.ElementTree):
        self.tree = tree

    @property
    def genre_taxonomy(self) -> etree.Element:
        xpath = ".//tei:encodingDesc//tei:category[@xml:id='genre']"
        return find_node(tree=self.tree, xpath=xpath)


class ParserProfileDesc:
    """Branch of XML tree at teiHeader/profileDesc."""

    def __init__(self, tree):
        self.tree = tree

    @property
    def creation(self) -> etree.Element:
        xpath = ".//tei:profileDesc/tei:creation"
        return find_node(tree=self.tree, xpath=xpath)

    @property
    def languUsage(self) -> etree.Element:
        xpath = ".//tei:profileDesc/tei:langUsage"
        return find_node(tree=self.tree, xpath=xpath)


class ParserTextTEI_XML:
    def __init__(self, base_file: str = TEXT_TEI_MODEL):
        self.tree = etree.parse(base_file)
        self.titleStmt = ParserTitleStmt(tree=self.tree)
        self.publicationStmt = ParserPublicationStmt(tree=self.tree)
        self.encodingDesc = ParserEncodingDesc(tree=self.tree)
        self.profileDesc = ParserProfileDesc(tree=self.tree)
