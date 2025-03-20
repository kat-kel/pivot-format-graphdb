from typing import Optional
from pydantic import BaseModel, Field, computed_field
from app.database import DBConn
from dataclasses import dataclass


class Images(BaseModel):
    dig_id: int = Field(
        alias="contained_in H-ID",
    )
    first_image: int
    last_image: Optional[int] = Field(default=None)
    corresponding_page_range: str

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"images_{self.id}"

    @computed_field
    @property
    def sequence(self) -> list[int]:
        """Create list of image file numbers

        Examples:
        >>> data = {"contained_in H-ID": 1, "first_image": 1, "last_image": 10}
        >>> data.update({"corresponding_page_range": "1-5"})
        >>> i = Images(**data)
        >>> i.sequence
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        Returns:
            list[int]: _description_
        """
        if self.last_image:
            seq = list(range(self.first_image, self.last_image)) + [self.last_image]
        else:
            seq = [self.first_image]
        return seq


@dataclass
class PageRange:
    text: str
    start: Optional[str] = None
    end: Optional[str] = None
    images: Optional[Images] = None

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"pages_{self.id}"

    @classmethod
    def validate(self, page_str: str, part_id: int, db: DBConn) -> "PageRange":
        # Get beginning and end of page range
        extremes = page_str.split("-")
        end, start = None, None
        if len(extremes) == 2 and " " not in extremes[-1]:
            end = extremes[-1]
        if " " not in extremes[0]:
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
                return PageRange(text=page_str, start=start, end=end, images=model)

        return PageRange(text=page_str, start=start, end=end)
