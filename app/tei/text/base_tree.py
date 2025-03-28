from lxml import etree
from app.constants import NSMAP


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
