"""Class for parsing elements of the tree of the text's TEI-XML document."""

from lxml import etree
from app import TEXT_TEI_MODEL
from datetime import datetime
from app.tei.text.base_tree import BaseTEIParser


class TextXMLParser:
    def __init__(self, base_file: str = TEXT_TEI_MODEL):
        self.tree = etree.parse(base_file)
        self.titleStmt = self.TitleStmtParser(tree=self.tree)
        self.publicationStmt = self.PublicationStmtParser(tree=self.tree)
        self.encodingDesc = self.EncodingDescParser(tree=self.tree)
        self.profileDesc = self.ProfileDescParser(tree=self.tree)

    class TitleStmtParser(BaseTEIParser):
        """Branch of XML tree at teiHeader/fileDesc/titleStmt."""

        def __init__(self, tree: etree.ElementTree):
            self.tree = tree
            super().__init__(tree=tree)

        @property
        def title(self) -> etree.Element:
            xpath = "//tei:titleStmt/tei:title"
            return self.__find_node__(xpath=xpath)

        @property
        def respStmt(self) -> etree.Element:
            xpath = "//tei:titleStmt/tei:respStmt"
            return self.__find_node__(xpath=xpath)

    class PublicationStmtParser(BaseTEIParser):
        """Branch of XML tree at teiHeader/fileDesc/publicationStmt."""

        def __init__(self, tree: etree.ElementTree):
            self.tree = tree
            self.date.text = datetime.now().strftime("%Y-%m-%d")
            super().__init__(tree=tree)

        @property
        def date(self) -> etree.Element:
            xpath = "//tei:publicationStmt/tei:date"
            return self.__find_node__(xpath=xpath)

    class EncodingDescParser(BaseTEIParser):
        """Branch of XML tree at teiHeader/encodingDesc."""

        def __init__(self, tree: etree.ElementTree):
            self.tree = tree
            super().__init__(tree=tree)

        @property
        def genre_taxonomy(self) -> etree.Element:
            xpath = "//tei:encodingDesc//tei:category[@xml:id='genre']"
            return self.__find_node__(xpath=xpath)

    class ProfileDescParser(BaseTEIParser):
        """Branch of XML tree at teiHeader/profileDesc."""

        def __init__(self, tree):
            self.tree = tree
            super().__init__(tree=tree)

        @property
        def creation(self) -> etree.Element:
            xpath = "//tei:profileDesc/tei:creation"
            return self.__find_node__(xpath=xpath)

        @property
        def languUsage(self) -> etree.Element:
            xpath = "//tei:profileDesc/tei:langUsage"
            return self.__find_node__(xpath=xpath)
