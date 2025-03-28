from lxml import etree
from dataclasses import dataclass
from app import CONTRIBUTORS
from app.tei.text import TextTree
from app.models.data import TextDataModel


@dataclass
class RespPerson:
    """Class to manage metadata for individuals listed in the 'respStmt' node."""

    name: str
    role: str

    def insert_nodes(self, parent: etree.Element) -> None:
        """As sub-elements of respStmt, insert 2 nodes about individuals'
        responsibility: name (<name>) and role (<resp>).

        Args:
            parent (etree.Element): respStmt node in the titleStmt.
        """
        name_node = etree.SubElement(parent, "name")
        name_node.text = self.name
        role_node = etree.SubElement(parent, "resp")
        role_node.text = self.role


@dataclass
class TitleStmt:
    """Class to manage construction of nodes in 'teiHeader/fileDesc/titleStmt' branch.\
        """

    respStmt: list[RespPerson]
    title: str | None = None

    @classmethod
    def load_data_model(cls, text: TextDataModel) -> "TitleStmt":
        """Parse metadata from the text data model that are relevant to elements \
            in the 'teiHeader/fileDesc/titleStmt' branch.

        Args:
            text (TextDataModel): Text data model.

        Returns:
            TitleStmt: Parsed metadata from the text data model.
        """

        if text.language:
            lang_code = text.language.code
        else:
            lang_code = None

        resp_people = cls.load_responsibility_config(language_code=lang_code)
        return TitleStmt(
            title=text.name,
            respStmt=resp_people,
        )

    @classmethod
    def insert_data(cls, text: TextDataModel, tree: TextTree) -> None:
        """Transform the text data model's metadata into the elements in the \
            'teiHeader/fileDesc/titleStmt' branch and insert them into the tree.

        Args:
            text (TextDataModel): Text data model.
            tei_tree (etree.ElementTree): Tree of the text's TEI document.
        """
        # Parse metadata from the text data model
        data = cls.load_data_model(text=text)

        # Set the titleStmt title
        title_node = tree.titleStmt.title
        title_node.text = f'Encoded metadata of "{data.title}"'

        # Set the titleStmt respStmt
        resp_node = tree.titleStmt.respStmt
        for person in data.respStmt:
            person.insert_nodes(parent=resp_node)

    @staticmethod
    def load_responsibility_config(language_code: str | None) -> list[RespPerson]:
        """From the project's config yaml, load details about individuals'
        responsibility for various components of the data and encoding.

        Args:
            language_code (str | None): ISO code of the text's language.

        Returns:
            list[RespPerson]: Modelled metadata of people responsible for TEI document.
        """

        # Start list of people with data entry and proof correction contributors
        languages = CONTRIBUTORS["data entry"]
        if language_code and languages.get(language_code):
            names = languages[language_code]
        else:
            names = languages["default"]
        people = [
            RespPerson(name=n, role="data entry and proof correction") for n in names
        ]

        # Extend list with people responsible for metadata's TEI markup
        people.extend(
            [
                RespPerson(name=n, role="conversion of metadata to TEI markup")
                for n in CONTRIBUTORS["encoding"]["metadata"]
            ]
        )

        # Extend list with people responsible for text transcription's TEI markup
        people.extend(
            [
                RespPerson(name=n, role="conversion of text to TEI markup")
                for n in CONTRIBUTORS["encoding"]["text"]
            ]
        )

        return people
