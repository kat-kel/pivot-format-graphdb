import xml.etree.ElementTree as ET
import datetime


class PublicationStmt:
    def __init__(self):
        self.root = ET.Element("publicationStmt")
        self.root.append(self.publisher)
        self.root.append(self.pubPlace)
        self.root.append(self.date)
        self.root.append(self.availability)

    @property
    def publisher(self) -> ET.Element:
        elem = ET.Element("publisher")
        elem.text = "LostMa ERC Project"
        return elem

    @property
    def pubPlace(self) -> ET.Element:
        elem = ET.Element("pubPlace")
        elem.text = "Paris"
        return elem

    @property
    def date(self) -> ET.Element:
        today = datetime.date.today().strftime("%Y-%m-%d")
        elem = ET.Element("date")
        elem.text = today
        return elem

    @property
    def availability(self) -> ET.Element:
        elem = ET.Element("availablility", attrib={"status": "restricted"})
        url = "https://creativecommons.org/licenses/by/4.0/"
        licence = ET.SubElement(elem, "licence", attrib={"target": url})
        licence.text = (
            "Distributed under a Creative Commons Attribution 4.0 International License"
        )
        return elem
