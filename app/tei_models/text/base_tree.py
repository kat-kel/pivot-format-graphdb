"""Class for parsing elements of the tree of the text's TEI-XML document."""

from lxml import etree
from app.constants import NSMAP
from config import TEXT_BASE_FILE
from datetime import datetime


class BaseTEIParser(object):
    def __init__(self, tree: etree.ElementTree):
        self.tree = tree

    def __find_node__(self, xpath: str) -> etree.Element:
        """Find a specific node in the XML tree.

        Args:
            xpath (str): Xpath with 'tei:' namespace before each tag name.

        Raises:
            IndexError: Error indicating the xpath didn't find 1 specific node.

        Returns:
            etree.Element: The targeted node in the tree.
        """

        matches = self.tree.xpath(xpath, namespaces=NSMAP)
        if len(matches) != 1:
            raise IndexError()
        else:
            return matches[0]


class TextTree:
    def __init__(self, base_file: str = TEXT_BASE_FILE):
        self.tree = etree.parse(base_file)
        self.titleStmt = self.TitleStmt(tree=self.tree)
        self.publicationStmt = self.PublicationStmt(tree=self.tree)
        self.encodingDesc = self.EncodingDesc(tree=self.tree)
        self.profileDesc = self.ProfileDesc(tree=self.tree)

    class TitleStmt(BaseTEIParser):
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

    class PublicationStmt(BaseTEIParser):
        """Branch of XML tree at teiHeader/fileDesc/publicationStmt."""

        def __init__(self, tree: etree.ElementTree):
            self.tree = tree
            self.date.text = datetime.now().strftime("%Y-%m-%d")
            super().__init__(tree=tree)

        @property
        def date(self) -> etree.Element:
            xpath = "//tei:publicationStmt/tei:date"
            return self.__find_node__(xpath=xpath)

    class EncodingDesc(BaseTEIParser):
        """Branch of XML tree at teiHeader/encodingDesc."""

        def __init__(self, tree: etree.ElementTree):
            self.tree = tree
            super().__init__(tree=tree)

        @property
        def genre_taxonomy(self) -> etree.Element:
            xpath = "//tei:encodingDesc//tei:category[@xml:id='genre']"
            return self.__find_node__(xpath=xpath)

    class ProfileDesc(BaseTEIParser):
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
