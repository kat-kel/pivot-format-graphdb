import xml.etree.ElementTree as ET
from app.models.part import PartModel
from app.constants import XML_ID


class MsItem:
    def __init__(self, part: PartModel) -> None:
        self.root = ET.Element(
            "msItem",
            attrib={
                XML_ID: f"part-{part.id}",
                "n": str(part.div_order),
            },
        )
        # Add locus for manuscript item (part)
        locusGrp = ET.SubElement(self.root, "locusGrp", attrib={"scheme": "#source"})
        has_digital_facsimile = False
        for pr in part.page_ranges:
            if pr.images:
                has_digital_facsimile = True
            locus = ET.SubElement(locusGrp, "locus")
            if pr.start and pr.end:
                locus.set("from", pr.start)
                locus.set("to", pr.end)
            locus.text = pr.text

        # Add corresponding locus for digitization images
        if has_digital_facsimile:
            locusGrp = ET.SubElement(
                self.root, "locusGrp", attrib={"scheme": "#facsimile"}
            )
            for pr in part.page_ranges:
                if pr.images:
                    images = pr.images
                    locus = ET.SubElement(locusGrp, "locus")
                    if images.first_image and images.last_image:
                        locus.set("from", str(images.first_image))
                        locus.set("to", str(images.last_image))
                        locus.text = f"{images.first_image}-{images.last_image}"
                    else:
                        locus.set("from", str(images.first_image))
                        locus.set("to", str(images.first_image))
                        locus.text = str(images.first_image)

        # Add note describing what part of the text this item contains
        note = ET.SubElement(self.root, "note")
        note.text = part.part_of_text
