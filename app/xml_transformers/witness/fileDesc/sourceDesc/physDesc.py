import xml.etree.ElementTree as ET
from app.models.part import PartModel
from app.constants import XML_ID


class PhysDesc:
    data = None

    def __init__(self, parts: list[PartModel]) -> ET.Element:
        self.root = ET.Element("physDesc")

        if self.has_physDesc(parts=parts):
            self.data = parts[0].physical_description
            self.root.set(XML_ID, f"physdesc-{self.data.id}")

            # Append objectDesc
            self.root.append(self.objectDesc)

    @staticmethod
    def has_physDesc(parts) -> bool:
        # Confirm that the document's parts only have one physDesc
        # This script is not adapted to handling multiple physDesc for a
        # witness's multiple parts in a document
        physdesc_ids = set()
        has_physDesc = False
        for part in parts:
            if part.physical_description:
                has_physDesc = True
                physdesc_ids.add(part.physical_description.id)
        if has_physDesc:
            try:
                assert len(physdesc_ids) == 1
            except Exception:
                from pprint import pprint

                pprint([p.model_dump() for p in parts])
                raise Exception(">1 physDesc for this document's parts")
        return has_physDesc

    @property
    def objectDesc(self) -> ET.Element:
        objectDesc = ET.SubElement(self.root, "objectDesc")
        if self.data.form:
            objectDesc.set("form", self.data.form.label)

        supportDesc = ET.SubElement(objectDesc, "supportDesc")
        if self.data.material:
            supportDesc.set("material", self.data.material.label)

        if self.data.folio_size_height or self.data.folio_size_width:
            height, width = self.data.folio_size_height, self.data.folio_size_width
            extent = ET.SubElement(supportDesc, "extent")
            dimensions = ET.SubElement(
                extent,
                "dimensions",
                attrib={
                    "scope": "all",
                    "type": "current",
                    "unit": "millimeters",
                },
            )
            if height:
                _ = ET.SubElement(
                    dimensions,
                    "height",
                    attrib={"quantity": height},
                )
            if width:
                _ = ET.SubElement(dimensions, "width", attrib={"quantity": width})

        if (
            self.data.estimated_folio_size_height
            or self.data.estimated_folio_size_width
        ):
            height, width = (
                self.data.estimated_folio_size_height,
                self.data.estimated_folio_size_width,
            )
            extent = ET.SubElement(supportDesc, "extent")
            dimensions = ET.SubElement(
                extent,
                "dimensions",
                attrib={
                    "scope": "all",
                    "cert": "estimation",
                    "type": "original",
                    "unit": "millimeters",
                },
            )
            if height:
                _ = ET.SubElement(
                    dimensions,
                    "height",
                    attrib={"quantity": height},
                )
            if width:
                _ = ET.SubElement(dimensions, "width", attrib={"quantity": width})

        return objectDesc
