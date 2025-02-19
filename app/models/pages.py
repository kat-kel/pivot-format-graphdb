from typing import Optional
from pydantic import BaseModel, Field
from app.database import DBConn
from dataclasses import dataclass


class Images(BaseModel):
    dig_id: int = Field(validation_alias="contained_in H-ID")
    first_image: int
    last_image: int
    corresponding_page_range: str


@dataclass
class PageRange:
    start: str
    end: Optional[str] = None
    images: Optional[Images] = None

    @classmethod
    def validate(self, page_str: str, part_id: int, db: DBConn) -> "PageRange":
        # Get beginning and end of page range
        extremes = page_str.split("-")
        end = None
        if len(extremes) == 2:
            end = extremes[-1]
        start = extremes[0]

        # Get image entities that link to this part
        query = f"""
SELECT i.* FROM Images i WHERE i."represents_pages H-ID" = {part_id}
"""
        for image_match in db.select_all(query=query):
            model = Images(**image_match)
            # Because a part can have more than 1 page range string,
            # try to match the image sequence to the page range
            page_parts = model.corresponding_page_range.split("-")
            if (
                start.strip() == page_parts[0].strip()
                or end.strip() == page_parts[-1].strip()
            ):
                return PageRange(start=start, end=end, images=model)

        return PageRange(start=start, end=end)
