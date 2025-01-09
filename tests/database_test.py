import json
import unittest
from datetime import datetime

from src.backend.constants import HeuristDB
from src.backend.database import DB


def convert_datetime(d: dict) -> dict:
    clean_dict = {}
    for k, v in d.items():
        if isinstance(v, list) and isinstance(v[0], datetime):
            clean_dict.update({k: [str(i) for i in v]})
        elif isinstance(v, datetime):
            clean_dict.update({k: str(v)})
        else:
            clean_dict.update({k: v})
    return clean_dict


class TestProcess(unittest.TestCase):
    def setUp(self):
        self.db = DB()

    def test(self):
        witnesses = self.db.select(f"select * from {HeuristDB.witness}")

        collections = {}

        for w in witnesses:
            w = convert_datetime(w)

            text_id = w["is_manifestation_of H-ID"]

            if not collections.get(text_id):
                text = self.db.select(
                    f"""select * from {HeuristDB.text} where "H-ID" = {text_id}"""
                )[0]
                collections.update({text_id: {"text metadata": convert_datetime(text)}})
                collections[text_id].update({"text witnesses": {}})

            part_id = w.pop("observed_on_pages H-ID")
            query = f"""select * from {HeuristDB.part} where "H-ID" = {part_id}"""
            parts = self.db.select(query)

            w.update({"text parts": {}})

            for p in parts:
                p = convert_datetime(p)

                physdesc_id = p.pop("physical_description H-ID")
                if physdesc_id:
                    physdesc = self.db.select(
                        f"""select * from {HeuristDB.physDesc} where "H-ID" = {physdesc_id}"""
                    )[0]
                    p.update({"physical_description": convert_datetime(physdesc)})

                doc_id = p.pop("is_inscribed_on H-ID")
                doc = self.db.select(
                    f"""select * from {HeuristDB.document} where "H-ID" = {doc_id}"""
                )[0]
                p.update({"document": convert_datetime(doc)})

                w["text parts"].update({f"part {int(p["div_order"])}": p})

            collections[text_id]["text witnesses"].update({f"witness {w["H-ID"]}": w})

        obj = {"texts": {f"text {k}": v for k, v in collections.items()}}

        with open("tests/textCollections.json", "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
