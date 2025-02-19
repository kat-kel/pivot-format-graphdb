import xml.etree.ElementTree as ET
from app.models.witness import WitnessModel


class ProfileDesc:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("profileDesc")
