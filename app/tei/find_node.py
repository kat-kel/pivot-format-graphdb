from lxml import etree

from app.constants import NSMAP


def find_node(tree: etree.ElementTree, xpath: str) -> etree.Element:
    """Find a specific node in the XML tree.

    Args:
        tree (etree.ElementTree): Tree.
        xpath (str): Xpath with 'tei:' namespace before each tag name.

    Raises:
        IndexError: Error indicating the xpath didn't find 1 specific node.

    Returns:
        etree.Element: The targeted node in the tree.
    """

    matches = tree.xpath(xpath, namespaces=NSMAP)
    if len(matches) != 1:
        raise IndexError()
    else:
        return matches[0]


def iterate_nodes(tree: etree.ElementTree, xpath: str):
    yield from tree.xpath(xpath, namespaces=NSMAP)
