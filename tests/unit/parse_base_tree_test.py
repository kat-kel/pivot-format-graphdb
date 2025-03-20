import unittest
from lxml import etree
from datetime import datetime
from app.data_models.text import TextModel
from app.data_models.date import DateObject
from app.data_models.genre import GenreModel
from app.database import DBConn
from heurist.converters.date_handler import HeuristDateHandler
from app.data_models.term import TermModel
from app.constants import NSMAP, XML_ID
from config import CONTRIBUTOR_CONFIG, TEXT_BASE_FILE


class BaseParser:
    ns = NSMAP

    def __init__(self, base_file: str):
        self.tree = etree.parse(base_file)
        self.root = self.tree.getroot()

    @property
    def title(self) -> etree.Element:
        matches = self.tree.xpath("//tei:titleStmt/tei:title", namespaces=self.ns)
        return matches[0]

    @property
    def respStmt(self) -> etree.Element:
        matches = self.tree.xpath("//tei:titleStmt/tei:respStmt", namespaces=self.ns)
        return matches[0]

    @property
    def creation_date(self) -> etree.Element:
        matches = self.tree.xpath(
            "//tei:profileDesc/tei:creation/tei:date", namespaces=self.ns
        )
        return matches[0]

    @property
    def language(self) -> etree.Element:
        matches = self.tree.xpath("//tei:profileDesc//tei:language", namespaces=self.ns)
        return matches[0]

    @property
    def genre_taxonomy_category(self) -> etree.Element:
        xpath = "//tei:encodingDesc//tei:category[@xml:id='genre']"
        matches = self.tree.xpath(xpath, namespaces=self.ns)
        return matches[0]

    def set_file_date(self) -> None:
        matches = self.tree.xpath("//tei:publicationStmt/tei:date", namespaces=self.ns)
        node = matches[0]
        node.text = datetime.now().strftime("%Y-%m-%d")

    def set_text_title(self, title: str) -> None:
        node = self.title
        node.text = f'Encoded metadata of "{title}"'

    def set_resp_stmt(self, language: str | None) -> None:
        languages = CONTRIBUTOR_CONFIG["data entry"]
        metadata = CONTRIBUTOR_CONFIG["encoding"]["metadata"]
        text = CONTRIBUTOR_CONFIG["encoding"]["text"]

        if language and languages.get(language.code):
            data_entry = languages[language.code]
        else:
            data_entry = languages["default"]

        parent = self.respStmt
        for name in data_entry:
            name_node = etree.SubElement(parent, "name")
            name_node.text = name
            resp_node = etree.SubElement(parent, "resp")
            resp_node.text = "data entry and proof correction"

        for name in metadata:
            name_node = etree.SubElement(parent, "name")
            name_node.text = name
            resp_node = etree.SubElement(parent, "resp")
            resp_node.text = "conversion of metadata to TEI markup"

        for name in text:
            name_node = etree.SubElement(parent, "name")
            name_node.text = name
            resp_node = etree.SubElement(parent, "resp")
            resp_node.text = "conversion of text to TEI markup"

    def set_language(self, language_term: TermModel | None) -> None:
        if not language_term:
            return
        node = self.language
        node.attrib["ident"] = language_term.code
        if language_term.semantic_reference:
            node.attrib["ref"] = language_term.semantic_reference
        else:
            node.attrib["ref"] = ""
        node.text = language_term.description

    def set_text_date(self, date: DateObject | None, date_freetext: str | None) -> None:
        node = self.creation_date

        node.attrib["notBefore"] = ""
        node.attrib["notAfter"] = ""
        node.attrib["cert"] = ""

        if date:
            if date.estMinDate:
                node.attrib["notBefore"] = HeuristDateHandler.fill_out_date_str(
                    date.estMinDate
                )
            if date.estMaxDate:
                node.attrib["notAfter"] = HeuristDateHandler.fill_out_date_str(
                    date.estMaxDate
                )
            if date.determination:
                node.attrib["cert"] = date.determination
        if date_freetext:
            node.text = date_freetext

    def set_genre(self, genre: GenreModel | None) -> None:
        if not genre:
            return

        def make_cateogry(genre: GenreModel) -> etree.Element:
            cat = etree.Element("category")
            cat.set(XML_ID, genre.xml_id)
            catDesc = etree.SubElement(cat, "catDesc")
            catDesc.text = genre.preferred_name
            return cat

        base_category = make_cateogry(genre=genre)

        # Nesting genres currently only works with a single parent-child relationship.
        if genre.parent_genre:
            parent_category = make_cateogry(genre=genre.parent_genre)
            parent_category.append(base_category)
            self.genre_taxonomy_category.append(parent_category)

        # If there is no parent, directly append the genre to the genre category.
        else:
            self.genre_taxonomy_category.append(base_category)

    def set_text_metadata(self, text: TextModel) -> None:
        title = text.preferred_name
        lang = text.language
        date = text.date_of_creation

        self.set_file_date()
        self.set_text_title(title=title)
        self.set_resp_stmt(language=lang)
        self.set_text_date(date=date, date_freetext=text.date_freetext)
        self.set_language(language_term=text.language)
        self.set_genre(genre=text.genre)

    def write(self, fp: str) -> None:
        etree.indent(self.tree)
        s = etree.tostring(
            self.tree, encoding="utf-8", xml_declaration=True, pretty_print=True
        )
        with open(fp, "wb") as f:
            f.write(s)


class BaseParserTest(unittest.TestCase):
    def setUp(self):
        db = DBConn()
        record = db.select_all(
            """
SELECT * FROM TextTable
WHERE "specific_genre H-ID" IS NOT NULL
"""
        )[0]
        nested_dict = TextModel.build_nested_dict(row_dict=record, db=db)
        self.text = TextModel(**nested_dict)

    def test(self):
        bp = BaseParser(base_file=TEXT_BASE_FILE)

        bp.set_text_metadata(text=self.text)

        bp.write(fp="output.xml")


if __name__ == "__main__":
    unittest.main()
