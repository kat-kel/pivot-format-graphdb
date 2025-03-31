"""Class for parsing elements of the tree of the text's TEI-XML document."""

from datetime import datetime

from lxml import etree

from app import TEXT_TEI_MODEL
from app.tei.find_node import find_node


class TitleStmtParser:
    """Branch of XML tree at teiHeader/fileDesc/titleStmt."""

    def __init__(self, tree: etree.ElementTree):
        self.tree = tree

    @property
    def title(self) -> etree.Element:
        xpath = "//tei:titleStmt/tei:title"
        return find_node(tree=self.tree, xpath=xpath)

    @property
    def respStmt(self) -> etree.Element:
        xpath = "//tei:titleStmt/tei:respStmt"
        return find_node(tree=self.tree, xpath=xpath)


class PublicationStmtParser:
    """Branch of XML tree at teiHeader/fileDesc/publicationStmt."""

    def __init__(self, tree: etree.ElementTree):
        self.tree = tree
        self.date.text = datetime.now().strftime("%Y-%m-%d")

    @property
    def date(self) -> etree.Element:
        xpath = "//tei:publicationStmt/tei:date"
        return find_node(tree=self.tree, xpath=xpath)


class EncodingDescParser:
    """Branch of XML tree at teiHeader/encodingDesc."""

    def __init__(self, tree: etree.ElementTree):
        self.tree = tree

    @property
    def genre_taxonomy(self) -> etree.Element:
        xpath = "//tei:encodingDesc//tei:category[@xml:id='genre']"
        return find_node(tree=self.tree, xpath=xpath)


class ProfileDescParser:
    """Branch of XML tree at teiHeader/profileDesc."""

    def __init__(self, tree):
        self.tree = tree

    @property
    def creation(self) -> etree.Element:
        xpath = "//tei:profileDesc/tei:creation"
        return find_node(tree=self.tree, xpath=xpath)

    @property
    def languUsage(self) -> etree.Element:
        xpath = "//tei:profileDesc/tei:langUsage"
        return find_node(tree=self.tree, xpath=xpath)


class TextXMLParser:
    def __init__(self, base_file: str = TEXT_TEI_MODEL):
        self.tree = etree.parse(base_file)
        self.titleStmt = TitleStmtParser(tree=self.tree)
        self.publicationStmt = PublicationStmtParser(tree=self.tree)
        self.encodingDesc = EncodingDescParser(tree=self.tree)
        self.profileDesc = ProfileDescParser(tree=self.tree)
