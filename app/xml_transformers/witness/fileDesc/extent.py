from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET


class Extent:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = self.extent

    @property
    def extent(self) -> ET.Element:
        root = ET.Element("extent")

        # to-do: calculate pages in parts

        return root
