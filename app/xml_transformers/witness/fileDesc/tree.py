from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET
from .extent import Extent
from .sourceDesc import SourceDesc
from .titleStmt import TitleStmt
from .editionStmt import EditionStmt
from .publicationStmt import PublicationStmt


class WitnessFileDesc:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("fileDesc")

        # Add children of fileDesc
        titleStmt = TitleStmt(data=data).root
        self.root.append(titleStmt)

        editionStmt = EditionStmt().root
        self.root.append(editionStmt)

        publicationStmt = PublicationStmt().root
        self.root.append(publicationStmt)

        extent = Extent(data=data).root
        self.root.append(extent)

        sourceDesc = SourceDesc(data=data).root
        self.root.append(sourceDesc)
