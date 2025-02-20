from app.models.part import PartModel
import xml.etree.ElementTree as ET
from app.constants import XML_ID


class SourceDoc:
    def __init__(self, parts: list[PartModel]) -> None:
        self.data = self.sort_parts(data=parts)
        self.root = ET.Element("sourceDoc")

        for part in self.data:
            self.make_surfaces(part=part)

    @staticmethod
    def make_digitization_ref(dig_id: int, image_n: int) -> str:
        did = f"dig-{dig_id}"
        iid = f"image-{image_n}"
        return f"{did}-{iid}"

    @staticmethod
    def sort_parts(data: list[PartModel]) -> list[PartModel]:
        return sorted(data, key=lambda x: x.div_order, reverse=True)

    def make_surfaces(self, part: PartModel) -> None:
        for range in part.page_ranges:
            if range.images:
                dig_id = range.images.dig_id
                for n in range.images.sequence:
                    xml_id = self.make_digitization_ref(
                        dig_id=dig_id,
                        image_n=n,
                    )
                    corresp = f"#dig-{dig_id} #part-{part.id}"
                    surface = ET.Element(
                        "surface",
                        attrib={XML_ID: xml_id, "corresp": corresp},
                    )
                    self.root.append(surface)
