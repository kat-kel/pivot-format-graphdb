from lxml import etree

from app.data_models.text import TextModel
from app.tei_models.text.base_tree import TextTree
from app.data_models.term import TermModel
from app.data_models.date import DateObject, DeterminationConverter
from heurist.converters.date_handler import HeuristDateHandler
from dataclasses import dataclass


@dataclass
class Date:
    """Data model to manage metadata for 'teiHeader/profileDesc/creation/date' node."""

    notBefore: str = ""
    notAfter: str = ""
    cert: str = ""

    @classmethod
    def load_date(cls, date_obj: DateObject | None) -> "Date":
        """Parse metadata from the text's date of creation relevant to the 'date' \
            node in the 'teiHeader/profileDesc/creation' branch.

        Args:
            date_obj (DateObject | None): The text's date of creation.

        Returns:
            Date: Date metadata.
        """

        if not date_obj:
            return Date()

        attribs = {}
        if date_obj.estMinDate:
            notBefore = HeuristDateHandler.fill_out_date_str(date_obj.estMinDate)
            attribs.update({"notBefore": notBefore})
        if date_obj.estMaxDate:
            notAfter = HeuristDateHandler.fill_out_date_str(date_obj.estMaxDate)
            attribs.update({"notAfter": notAfter})
        if date_obj.determination:
            cert = DeterminationConverter.convert(date_obj.determination)
            attribs.update({"cert": cert})
        return Date(**attribs)

    @classmethod
    def build_node(
        cls,
        date_obj: DateObject | None,
        freetext: str | None,
    ) -> etree.Element:
        """Build 'date' node for the branch 'teiHeader/profileDesc/creation/'.

        Args:
            date_obj (DateObject | None): Text's date of creation.
            freetext (str | None): Freetext describing text's date of creation.

        Returns:
            etree.Element: 'date' node.
        """

        date = Date.load_date(date_obj=date_obj)
        attribs = date.__dict__
        node = etree.Element("date", attrib=attribs)
        node.text = freetext or ""
        return node


@dataclass
class Language:
    """Data model to manage metadata for 'teiHeader/profileDesc/langUsage/language' \
        node."""

    ident: str = ""
    ref: str = ""
    text: str = ""

    @classmethod
    def load_term(cls, language: TermModel | None) -> "Language":
        """If the text has a language, parse the metadata that's relevant to the \
            'teiHeader/profileDesc/langUsage/language' node.

        Args:
            language (TermModel | None): Text's language.

        Returns:
            Language: Data model for the text's relevant language.
        """

        if not language:
            return Language()
        else:
            return Language(
                ident=language.code or "",
                text=language.description or "",
                ref=language.semantic_reference or "",
            )

    @classmethod
    def build_node(cls, term: TermModel | None) -> etree.Element:
        """Build 'language' node for the branch 'teiHeader/profileDesc/langUsage'.

        Args:
            term (TermModel | None): The text's language.

        Returns:
            etree.Element: 'language' node.
        """

        data = cls.load_term(language=term)
        node = etree.Element("language", {"ident": data.ident, "ref": data.ref})
        node.text = data.text
        return node


class ProfileDesc:
    """Class to manage construction of nodes in 'teiHeader/profileDesc' branch."""

    @classmethod
    def insert_data(cls, text: TextModel, tree: TextTree) -> None:
        """Transform the text data model's metadata into the elements in the \
            'teiHeader/profileDesc' branch and insert them into the tree.

        Args:
            text (TextModel): Text data model.
            tree (TextTree): Tree parser for the text's TEI document.
        """

        # Add a <date> node to the <creation> element
        date_node = Date.build_node(
            date_obj=text.date_of_creation, freetext=text.date_freetext
        )
        tree.profileDesc.creation.append(date_node)

        # Add a <language> nmode to the <langUsage> element
        lang_node = Language.build_node(term=text.language)
        tree.profileDesc.languUsage.append(lang_node)
